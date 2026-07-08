from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, CensusForm, CensusRecordFormSet, PiggeryCensusRecordFormSet
from drugapp.models import Dispatch, Drug, InventoryLog
from django.utils.timezone import localtime, now, localdate, timedelta
from django.db.models import Q, Prefetch, Max
from itertools import chain, zip_longest
from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from farmrecord.models import EventType, Census, Animals, PendingEventEdit, AnimalType, CensusRecord, CensusApprovalQueue, PiggeryCensusRecord, PiggeryLine
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.template.loader import render_to_string
from datetime import timedelta
import json
from django.forms.models import model_to_dict
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from itertools import zip_longest

User = get_user_model()
# Create your views here.

@login_required
def vet_index(request):
    today = localdate()
    now_time = now()
    last_24_hours = now_time - timedelta(hours=24)

    today_dispatches = Dispatch.objects.filter(dispatched_at__date=today)
    new_drugs = Drug.objects.filter(entered_at__gte=last_24_hours)
    restocked_logs = InventoryLog.objects.filter(
        updated_at__gte=last_24_hours,
        new_quantity__gt=F('previous_quantity')
    ).select_related('drug')
    restocked_drugs = Drug.objects.filter(id__in=restocked_logs.values_list('drug_id', flat=True))
    combined_new_drugs = list(set(chain(new_drugs, restocked_drugs)))
    # status = request.GET.get("status", "pending")
    # Get status filters independently
    event_status = request.GET.get("event_status", "pending")
    census_status = request.GET.get("census_status", "pending")

    # Pending edits
    pending_edits = PendingEventEdit.objects.filter(
        submitted_by=request.user,
        status=event_status
    ).select_related(
        "event", "event__animal", "event__animal_type", "reviewed_by"
    )


    for p in pending_edits:
        animal_id = p.data.get("animal")
        if animal_id:
            try:
                p.data["animal_obj"] = Animals.objects.get(id=animal_id)
            except Animals.DoesNotExist:
                p.data["animal_obj"] = None

        animal_type_id = p.data.get("animal_type")
        if animal_type_id:
            try:
                p.data["animal_type_obj"] = AnimalType.objects.get(id=animal_type_id)
            except AnimalType.DoesNotExist:
                p.data["animal_type_obj"] = None

    # 2. Fetch Census Changes based on current status filter
    is_processed_map = {
        "pending": False,
        "approved": True,
        "rejected": True
    }
    is_processed_val = is_processed_map.get(census_status, False)

    # 1. Start with the base query
    census_queries = CensusApprovalQueue.objects.filter(requested_by=request.user).select_related('census', 'census__animal')

    # 2. Filter based on status
    if census_status == "pending":
        census_queries = census_queries.filter(is_processed=False)
    elif census_status == "approved":
        census_queries = census_queries.filter(is_processed=True, approved=True)
    elif census_status == "rejected":
        census_queries = census_queries.filter(is_processed=True, approved=False)

    # 3. Add select_related
    census_queries = census_queries.select_related('census', 'census__animal')
    


    if census_status in ["approved", "rejected"]:
        approved_bool = True if census_status == "approved" else False
        census_queries = census_queries.filter(approved=approved_bool)

    # Hydrate JSON payloads with readable DB items for the template
    census_edits = []
    for queue_item in census_queries:
        payload = queue_item.form_data_payload or {}
        records_payload = payload.get('records', [])
        
        # Pull what currently lives in the DB for a side-by-side comparison
        db_records = {
            r.animal_type_id: r.number_of_animals 
            for r in queue_item.census.records.all()
        }

        processed_records = []
        for item in records_payload:
            type_id = item.get('animal_type')
            try:
                type_obj = AnimalType.objects.get(id=type_id)
                type_name = type_obj.animal_type_name
            except AnimalType.DoesNotExist:
                type_name = "Unknown Type"

            # Match up payloads with existing database baselines
            old_count = db_records.get(type_id, 0)
            
            processed_records.append({
                'animal_type_name': type_name,
                'new_count': item.get('number_of_animals', 0),
                'old_count': old_count,
                'is_deleted': item.get('DELETE', False)
            })

        census_edits.append({
            'queue_obj': queue_item,
            'census': queue_item.census,
            'main_form': payload.get('main_form', {}),
            'records': processed_records,
            'status': census_status
        })

    # -------------------- Latest census per animal --------------------
    profile = getattr(request.user, "profile", None)

    # Determine the vet section
    if profile.is_vet_piggery:
        animals_for_section = Animals.objects.filter(animal_name__iexact='pig')
    elif profile.is_vet_paddock:
        animals_for_section = Animals.objects.filter(animal_name__iexact='cattle')
    elif profile.is_vet_smallruminant:
        animals_for_section = Animals.objects.filter(animal_name__in=['sheep','goat'])
    else:
        animals_for_section = Animals.objects.none()

    # Get the latest census per animal
    census_list = []
    for animal in animals_for_section:
        last_census = (
            Census.objects
            .filter(animal=animal)
            .prefetch_related('records__animal_type')
            .order_by('-census_date')  # latest first
            .first()
        )
        if last_census:
            census_list.append(last_census)

    context = {
        'today_dispatches': today_dispatches,
        'today_date': today,
        'recent_drugs': combined_new_drugs,
        'event_edits': pending_edits,
        'census_edits': census_edits,
        # 'current_status': status,
        'current_event_status': event_status,
        'current_census_status': census_status,
        'census_list': census_list,
    }

    return render(request, 'vet/index.html', context)

@login_required
def dispatch_records_lazy(request):
    page = int(request.GET.get('page', 1))
    per_page = 10
    search = request.GET.get('search', '').strip()

    queryset = Dispatch.objects.select_related('drug', 'unit').order_by('-dispatched_at')

    if search:
        queryset = queryset.filter(drug__drug_name__icontains=search)

    paginator = Paginator(queryset, per_page)
    current_page = paginator.get_page(page)

    data = [
        {
            'drug': d.drug.drug_name,
            'quantity': d.quantity,
            'unit': d.unit.name,
            'dispatched_at': d.dispatched_at.strftime('%Y-%m-%d %H:%M'),
        }
        for d in current_page
    ]

    return JsonResponse({'results': data, 'has_next': current_page.has_next()})


@login_required
def dispatch_view(request):
  return render(request, 'vet/dispatch-records.html')




@login_required
def drugs_records_lazy(request):
  page = int(request.GET.get('page', 1))
  per_page = 10
  search = request.GET.get('search', '').strip()

  queryset = Drug.objects.select_related('unit').order_by('-entered_at')

  if search:
      queryset = queryset.filter(drug_name__icontains=search)

  paginator = Paginator(queryset, per_page)
  current_page = paginator.get_page(page)

  data = [
      {
        'manufacturer_name': d.manufacturer_name,
        'drug_name': d.drug_name,
        'batch_number': d.batch_number,
        'quantity': d.quantity,
        'unit': d.unit.name,
        'expiry_date': d.expiry_date.strftime('%Y-%m-%d'),
      }
      for d in current_page
  ]

  return JsonResponse({'results': data, 'has_next': current_page.has_next()})




@login_required
def drugs_view(request):
  return render(request, 'vet/drugs-records.html')


# @login_required
# def create_event(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST, request.FILES, user=request.user)

#         if form.is_valid():
#             event = form.save(commit=False)
#             event.save()

#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 action_type = request.POST.get('actionType')
#                 if action_type == 'proceed':
#                     return JsonResponse({
#                         'status': 'success',
#                         'message': 'Event saved successfully! Redirecting...',
#                         'redirect_url': reverse('veterinary:event_records')
#                     })
#                 return JsonResponse({
#                     'status': 'success',
#                     'message': 'Event saved successfully! You can add another.'
#                 })

#             messages.success(request, "Event created successfully!")
#             return redirect('veterinary:create_event')

#         else:
#             # Collect detailed field errors
#             errors = {
#                 field: [str(err) for err in errs]
#                 for field, errs in form.errors.items()
#             }

#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({
#                     'status': 'error',
#                     'message': 'Please correct the highlighted errors.',
#                     'errors': errors,
#                 })

#             messages.error(request, "Error saving event. Check your input.")

#     else:
#         form = EventForm(user=request.user)

#     return render(request, 'vet/event_form.html', {'form': form})


@login_required
def create_event(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        # ✅ Handle piggery location explicitly
        if getattr(request.user.profile, 'is_vet_piggery', False):
            line = request.POST.get('lineSelect', '')
            print(line)
            block = request.POST.get('blockSelect', '')
            pen = request.POST.get('penSelect', '')
            post_data['location'] = " ".join(filter(None, [line, block, pen]))
            # event.location = " ".join(filter(None, [line, block, pen]))
        # form = EventForm(request.POST, request.FILES, user=request.user)
        # form = EventForm(post_data, request.FILES, user=request.user)
        form = EventForm(post_data, request.FILES, user=request.user, edit_mode=False)
        print(form.errors)

        if form.is_valid():
            # event = form.save(commit=False)


            # event.save()
            event = form.save()

            # AJAX response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                action_type = request.POST.get('actionType')
                if action_type == 'proceed':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Event saved successfully! Redirecting...',
                        'redirect_url': reverse('veterinary:event_records')
                    })
                return JsonResponse({
                    'status': 'success',
                    'message': 'Event saved successfully! You can add another.'
                })

            # Non-AJAX redirect
            messages.success(request, "Event created successfully!")
            return redirect('veterinary:create_event')

        else:
            # Collect detailed field errors
            errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please correct the highlighted errors.',
                    'errors': errors,
                })

            messages.error(request, "Error saving event. Check your input.")

    else:
        form = EventForm(user=request.user)

    return render(request, 'vet/event_form.html', {'form': form, 'is_vet_piggery': request.user.profile.is_vet_piggery, 'event_model': EventType,})


@login_required
def event_records(request):
    user = request.user
    selected_event = request.GET.get('event_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page = request.GET.get('page', 1)

    events = EventType.objects.all().select_related('animal', 'animal_type')
    event_types = []

    if hasattr(user, 'profile'):
        profile = user.profile

        if profile.is_vet_piggery:
            events = events.filter(animal__animal_name='pig')
            event_types = ['culling', 'farrowing', 'gift', 'mortality', 'procurement', 'sale', 'treatment']

        elif profile.is_vet_paddock:
            events = events.filter(animal__animal_name='cattle')
            event_types = ['calving', 'gift', 'mortality', 'procurement', 'sale', 'treatment', 'vaccination']

        elif profile.is_vet_smallruminant:
            events = events.filter(animal__animal_name__in=['sheep', 'goat'])
            event_types = ['culling', 'gift', 'kidding', 'lambing', 'mortality', 'procurement', 'sale', 'treatment', 'vaccination']

        elif not profile.is_vet:
            events = EventType.objects.none()

    else:
        events = EventType.objects.none()

    # Filter by event type & date
    if selected_event:
        events = events.filter(event_name=selected_event)
    if start_date:
        events = events.filter(created_at__date__gte=parse_date(start_date))
    if end_date:
        events = events.filter(created_at__date__lte=parse_date(end_date))

    events = events.order_by('-event_date')

    # Pagination (10 items per scroll)
    paginator = Paginator(events, 2)
    page_obj = paginator.get_page(page)

    # If AJAX (scroll load)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('vet/event_records_list.html', {'events': page_obj})
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    context = {
        'events': page_obj,
        'event_types': event_types,
        'selected_event': selected_event,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'vet/entry-records.html', context)


# @login_required
# def event_detail(request, pk):
#   event = get_object_or_404(EventType.objects.select_related('animal', 'animal_type'), pk=pk)

#   context = {
#     'event': event
#   }
#   return render(request, 'vet/event_details.html', context)

@login_required
def event_detail(request, pk):
    event = get_object_or_404(EventType.objects.select_related('animal', 'animal_type'), pk=pk)
    
    # Check if this event already has a pending edit in the queue
    has_pending_edit = PendingEventEdit.objects.filter(event=event, status='pending').exists()

    context = {
        'event': event,
        'has_pending_edit': has_pending_edit, # Pass to template
    }
    return render(request, 'vet/event_details.html', context)



@login_required
def census_records(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page = request.GET.get('page', 1)

    vet_profile = request.user.profile
    
    # 1. Initialize the base queryset
    censuses = Census.objects.select_related('animal').order_by('-census_date')

    # 2. Apply filtering based on profile
    if vet_profile.is_vet_piggery:
        censuses = censuses.filter(animal__animal_name__iexact='pig').prefetch_related(
            Prefetch('piggery_records', queryset=PiggeryCensusRecord.objects.select_related('line'))
        )
    elif vet_profile.is_vet_paddock:
        censuses = censuses.filter(animal__animal_name__iexact='cattle').prefetch_related(
            Prefetch('records', queryset=CensusRecord.objects.select_related('animal_type'))
        )
    elif vet_profile.is_vet_smallruminant:
        censuses = censuses.filter(animal__animal_name__in=['sheep', 'goat']).prefetch_related(
            Prefetch('records', queryset=CensusRecord.objects.select_related('animal_type'))
        )
    else:
        censuses = Census.objects.none()

    # 3. Date range filters
    if start_date:
        censuses = censuses.filter(census_date__gte=parse_date(start_date))
    if end_date:
        end = parse_date(end_date)
        if end:
            censuses = censuses.filter(census_date__lt=end + timedelta(days=1))

    censuses = censuses.distinct()

    paginator = Paginator(censuses, 5)
    page_obj = paginator.get_page(page)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('vet/census_records_list.html', {'censuses': page_obj}, request=request)
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    return render(request, 'vet/census_records.html', {
        'censuses': page_obj,
        'start_date': start_date,
        'end_date': end_date,
    })


# @login_required
# def census_records(request):
#     """Display census records for the logged-in vet's section with date filters and no duplicates."""
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     page = request.GET.get('page', 1)

#     censuses = (
#         Census.objects
#         .select_related('animal')
#         .prefetch_related('records', 'records__animal_type')  # separate prefetch levels
#         .order_by('-census_date')
#     )

#     vet_profile = request.user.profile
#     queryset = Census.objects.select_related('animal').order_by('-census_date')

#     # if vet_profile.is_vet_piggery:
#     #     censuses = censuses.filter(animal__animal_name__iexact='pig')
#     if vet_profile.is_vet_piggery:
#         # Piggery uses piggery_records and PiggeryLine
#         queryset = queryset.filter(animal__animal_name__iexact='pig').prefetch_related(
#             Prefetch('piggery_records', queryset=PiggeryCensusRecord.objects.select_related('line'))
#         )
#     elif vet_profile.is_vet_paddock:
#         censuses = censuses.filter(animal__animal_name__iexact='cattle')
#     elif vet_profile.is_vet_smallruminant:
#         censuses = censuses.filter(animal__animal_name__in=['sheep', 'goat'])
#     elif not vet_profile.is_vet:
#         censuses = Census.objects.none()

#     # Date range filter
#     # Date range filter
#     if start_date:
#         censuses = censuses.filter(census_date__gte=parse_date(start_date))
#     if end_date:
#         end = parse_date(end_date)
#         if end:
#             censuses = censuses.filter(census_date__lt=end + timedelta(days=1))


#     # Ensure uniqueness
#     censuses = censuses.distinct()

#     paginator = Paginator(censuses, 5)
#     page_obj = paginator.get_page(page)

#     # AJAX infinite scroll
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         html = render_to_string('vet/census_records_list.html', {'censuses': page_obj})
#         return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

#     return render(request, 'vet/census_records.html', {
#         'censuses': page_obj,
#         'start_date': start_date,
#         'end_date': end_date,
#     })


# @login_required
# def create_census(request):

#     user = request.user

#     if request.method == 'POST':

#         form = CensusForm(request.POST, user=user)

#         formset = CensusRecordFormSet(
#             request.POST,
#             user=user,
#             prefix='records'
#         )

#         if form.is_valid() and formset.is_valid():

#             census = form.save()

#             records = formset.save(commit=False)

#             for record in records:
#                 record.census = census
#                 record.save()

#             census.update_total()

#             # messages.success(request,"Census created successfully.")

#             # return redirect('veterinary:census_records')
#             # return render(request, 'vet/census_form.html', {
#             #     'form': form,
#             #     'formset': formset,
#             #     'is_edit': False,
#             #     'existing_records': []
#             # })
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Census created successfully.'
#             })

#     else:

#         form = CensusForm(user=user)

#         formset = CensusRecordFormSet(
#             user=user,
#             prefix='records'
#         )

#         animal_type_qs = formset.form.base_fields['animal_type'].queryset

#     return render(
#         request,
#         'vet/census_form.html',
#         {
#             'form': form,
#             'formset': formset,
#             'animal_type_qs': animal_type_qs,
#             'is_edit': False,
#             'existing_records': []
#         }
#     )


@login_required
def create_census(request):
    user = request.user
    is_piggery = getattr(user.profile, 'is_vet_piggery', False)

    if request.method == 'POST':
        form = CensusForm(request.POST, user=user)
        # Select FormSet class based on user role
        FormSetClass = PiggeryCensusRecordFormSet if is_piggery else CensusRecordFormSet
        formset = FormSetClass(request.POST, user=user, prefix='records')

        if form.is_valid() and formset.is_valid():
            census = form.save()
            records = formset.save(commit=False)
            for record in records:
                record.census = census
                record.save()
            census.update_total()
            return JsonResponse({'status': 'success', 'message': 'Census created successfully.'})
    else:
        form = CensusForm(user=user)
        FormSetClass = PiggeryCensusRecordFormSet if is_piggery else CensusRecordFormSet
        formset = FormSetClass(user=user, prefix='records')

    return render(request, 'vet/census_form.html', {
        'form': form,
        'formset': formset,
        'is_edit': False,
        'existing_records': []
    })

# @login_required
# def edit_census(request, pk):
#     user = request.user
#     census = get_object_or_404(Census, pk=pk)
    
#     # Prevent modifications if a vet is already waiting for admin approval
#     # Robust check: Prevent modifications if a valid, unprocessed edit request exists
#     if census.is_pending_review:
#         # Check if an active record exists in the queue
#         active_request = CensusApprovalQueue.objects.filter(
#             census=census, 
#             is_processed=False
#         ).exists()
        
#         if active_request:
#             messages.error(request, "This census record is currently locked pending admin approval.")
#             return redirect('veterinary:census_records')
#         else:
#             # Sync state: Record was marked pending, but queue entry was deleted.
#             # Reset flag and allow user to proceed.
#             census.is_pending_review = False
#             census.save()
#     # if census.is_pending_review:
#     #     messages.error(request, "This census record is currently locked pending admin approval.")
#     #     return redirect('veterinary:vet_index')

#     if request.method == 'POST':
#         form = CensusForm(request.POST, instance=census, user=user)
#         formset = CensusRecordFormSet(request.POST, instance=census, user=user, prefix='records')

#         if form.is_valid() and formset.is_valid():
#             # Capture the user's note from the POST data
#             user_note = request.POST.get('request_note', '').strip()
            
#             # 1. Prepare serialized payload for the queue
#             serialized_payload = {
#                 'main_form': {
#                     'census_date': form.cleaned_data['census_date'].isoformat(),
#                     'notes': form.cleaned_data['notes'],
#                 },
#                 'records': [
#                     {
#                         'id': f.cleaned_data.get('id').id if f.cleaned_data.get('id') else None,
#                         'animal_type': f.cleaned_data['animal_type'].id,
#                         'number_of_animals': f.cleaned_data['number_of_animals'],
#                         'DELETE': f.cleaned_data.get('DELETE', False)
#                     }
#                     for f in formset.forms if f.has_changed() or f.cleaned_data.get('id')
#                 ]
#             }

#             # 2. Save to queue
#             # CensusApprovalQueue.objects.create(
#             #     census=census,
#             #     requested_by=user,
#             #     form_data_payload=serialized_payload,
#             #     request_note=user_note
#             # )

#             queue_item = CensusApprovalQueue.objects.create(
#                 census=census,
#                 requested_by=user,
#                 form_data_payload=serialized_payload,
#                 request_note=user_note
#             )

#             # # 3. Lock the record
#             # census.is_pending_review = True
#             # census.save()
#             # Generate identifier
#             request_id = f"SKAAL-CEN-{queue_item.id}"

#             # 3. Lock the record
#             census.is_pending_review = True
#             census.save()

#             # 4. Prepare data for email
#             old_records = [
#                 {'type': r.animal_type.animal_type_name, 'count': r.number_of_animals}
#                 for r in census.records.all()
#             ]
            
#             new_records = []
#             for item in serialized_payload['records']:
#                 try:
#                     type_obj = AnimalType.objects.get(id=item['animal_type'])
#                     type_name = type_obj.animal_type_name
#                 except AnimalType.DoesNotExist:
#                     type_name = "Unknown"
#                 new_records.append({'type': type_name, 'count': item['number_of_animals']})

#             combined_records = list(zip_longest(old_records, new_records, fillvalue=None))

#             # 5. Send Email
#             # subject = "New Census Edit Pending Approval"
#             subject = f"[{request_id}] New Census Edit Pending Approval"
#             context = {
#                 'vet_name': user.get_full_name(),
#                 'census_id': census.pk,
#                 'combined_records': combined_records,
#                 'review_url': request.build_absolute_uri(reverse('veterinary:vet_index')),
#                 'user_note': user_note,
#             }

#             html_content = render_to_string('emails/census_edit_status.html', context)
#             text_content = f"New census edit submitted by {user.get_full_name()} for Census #{census.pk}"
#             admin_emails = [u.email for u in User.objects.filter(profile__is_boss=True, is_active=True) if u.email]

#             if admin_emails:
#                 email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, admin_emails)
#                 email.attach_alternative(html_content, "text/html")
#                 email.send()

#             # messages.success(request, "Your updates have been submitted to the administrator for verification.")
#             # return redirect('veterinary:vet_index')
#             # Instead of just redirecting, return a success message
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({'status': 'success', 'message': 'Your updates have been submitted to the administrator for verification.'})
            
#             messages.success(request, "Your updates have been submitted to the administrator for verification.")
#             return redirect('veterinary:vet_index')

#     else:
#         form = CensusForm(instance=census, user=user)
#         formset = CensusRecordFormSet(instance=census, user=user, prefix='records')

#     existing_records = [
#         {
#             'id': record.id,
#             'typeId': record.animal_type.id,
#             'typeText': record.animal_type.animal_type_name,
#             'count': record.number_of_animals,
#         }
#         for record in census.records.all()
#     ]

#     return render(request, 'vet/census_form.html', {
#         'form': form,
#         'formset': formset,
#         'is_edit': True,
#         'census': census,
#         'existing_records': existing_records
#     })


@login_required
def edit_census(request, pk):
    user = request.user
    census = get_object_or_404(Census, pk=pk)
    
    # 1. Determine if this is a Piggery census
    is_piggery = getattr(user.profile, 'is_vet_piggery', False)
    FormSetClass = PiggeryCensusRecordFormSet if is_piggery else CensusRecordFormSet
    
    # 2. Lock check logic
    if census.is_pending_review:
        if CensusApprovalQueue.objects.filter(census=census, is_processed=False).exists():
            messages.error(request, "This census record is currently locked pending admin approval.")
            return redirect('veterinary:census_records')
        else:
            census.is_pending_review = False
            census.save()

    if request.method == 'POST':
        form = CensusForm(request.POST, instance=census, user=user)
        formset = FormSetClass(request.POST, instance=census, user=user, prefix='records')

        if form.is_valid() and formset.is_valid():
            user_note = request.POST.get('request_note', '').strip()
            
            # 3. Dynamic Payload Construction
            records_data = []
            for f in formset.forms:
                if f.has_changed() or f.cleaned_data.get('id'):
                    record_dict = {'DELETE': f.cleaned_data.get('DELETE', False)}
                    
                    if is_piggery:
                        record_dict.update({
                            'id': f.cleaned_data.get('id').id if f.cleaned_data.get('id') else None,
                            'line': f.cleaned_data['line'].id,
                            'number': f.cleaned_data['number'],
                            'piglets': f.cleaned_data.get('piglets', 0), # Capture this
                            'note': f.cleaned_data['note']
                        })
                    else:
                        record_dict.update({
                            'id': f.cleaned_data.get('id').id if f.cleaned_data.get('id') else None,
                            'animal_type': f.cleaned_data['animal_type'].id,
                            'number_of_animals': f.cleaned_data['number_of_animals']
                        })
                    records_data.append(record_dict)

            serialized_payload = {
                'main_form': {
                    'census_date': form.cleaned_data['census_date'].isoformat(),
                    'notes': form.cleaned_data['notes'],
                },
                'records': records_data
            }

            # 4. Save to Queue
            queue_item = CensusApprovalQueue.objects.create(
                census=census,
                requested_by=user,
                form_data_payload=serialized_payload,
                request_note=user_note
            )

            # 5. Lock and Notify
            census.is_pending_review = True
            census.save()
            request_id = f"SKAAL-CEN-{queue_item.id}"

            # Prepare email context
            # Note: You can add a similar check here to format Piggery records for the email
            subject = f"[{request_id}] New Census Edit Pending Approval"
            context = {
                'vet_name': user.get_full_name(),
                'census_id': census.pk,
                'review_url': request.build_absolute_uri(reverse('veterinary:vet_index')),
                'user_note': user_note,
            }

            html_content = render_to_string('emails/census_edit_status.html', context)
            admin_emails = [u.email for u in User.objects.filter(profile__is_boss=True, is_active=True) if u.email]

            if admin_emails:
                email = EmailMultiAlternatives(subject, f"New edit for #{census.pk}", settings.DEFAULT_FROM_EMAIL, admin_emails)
                email.attach_alternative(html_content, "text/html")
                email.send()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Your updates have been submitted to the administrator for verification.'})
            
            messages.success(request, "Your updates have been submitted to the administrator for verification.")
            return redirect('veterinary:vet_index')

    else:
        form = CensusForm(instance=census, user=user)
        formset = FormSetClass(instance=census, user=user, prefix='records')

    return render(request, 'vet/census_form.html', {
        'form': form,
        'formset': formset,
        'is_edit': True,
        'census': census,
    })

@login_required
def edit_event(request, pk):
    event = get_object_or_404(EventType, pk=pk)
    profile = getattr(request.user, 'profile', None)
    is_boss = profile and profile.is_boss

    # -------------------- AUTO-PARSE LOCATION FOR ALL SECTIONS --------------------
    initial_line = ""
    initial_block = ""
    initial_pen = ""

    initial_paddock = ""
    initial_small_ruminant = ""

    location = event.location.strip() if event.location else ""

    # Piggery: "Line X Block Y Pen Z"
    parts = location.split()
    if len(parts) == 6 and parts[0] == "Line":
        initial_line = f"{parts[0]} {parts[1]}"
        initial_block = f"{parts[2]} {parts[3]}"
        initial_pen = f"{parts[4]} {parts[5]}"

    # Paddock example: "Paddock 4" or "Paddock A"
    if location.startswith("Paddock"):
        initial_paddock = location

    # Small ruminant example: "SR Unit 2", "SR Pen 6"
    if location.lower().startswith("sr"):
        initial_small_ruminant = location
        print(initial_small_ruminant)

    

    # -------------------- PROCESS FORM --------------------
    if request.method == 'POST':
        # form = EventForm(request.POST, request.FILES, instance=event, user=request.user)
        original_data = {}

        for field in EventType._meta.fields:
            field_name = field.name
            original_data[field_name] = getattr(event, field_name)
        form = EventForm(request.POST, request.FILES, instance=event, user=request.user, edit_mode=True)
        if form.is_valid():

            if is_boss:
                updated_event = form.save(commit=False)
                updated_event.is_approved = True
                updated_event.save()
                message = "Event updated and approved successfully!"
            else:
                pending_data = {}

                for key, value in form.cleaned_data.items():
                    if key == 'edit_note':
                        continue
                    
                    if hasattr(value, 'pk'):
                        pending_data[key] = value.pk
                      
                    else:
                        pending_data[key] = value

                pending = PendingEventEdit.objects.create(
                    event=event,
                    submitted_by=request.user,
                    data=pending_data,
                    vet_note=form.cleaned_data.get('edit_note', '')
                )
                # ✅ Resolve FK objects for email (same as admin)
                animal_id = pending.data.get("animal")
                if animal_id:
                    try:
                        pending.data["animal_obj"] = Animals.objects.get(id=animal_id)
                    except Animals.DoesNotExist:
                        pending.data["animal_obj"] = None

                animal_type_id = pending.data.get("animal_type")
                if animal_type_id:
                    try:
                        pending.data["animal_type_obj"] = AnimalType.objects.get(id=animal_type_id)
                    except AnimalType.DoesNotExist:
                        pending.data["animal_type_obj"] = None

                request_id = f"SKAAL-EVT-{pending.id}"
                subject = f"[{request_id}] New Event Edit Pending Approval"
                context = {
                    'edit': pending,
                    'event': event,
                    'user': request.user,
                    'original_data': original_data,  # ✅ THIS is the fix
                    'note': pending.vet_note
                }

                html_content = render_to_string('emails/pending_event_edit.html', context)
                text_content = f"New edit submitted for event {event.event_name}"

                # Get admin emails (adjust as needed)
                admin_emails = [user.email for user in User.objects.filter(is_staff=True) if user.email]

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_FROM_EMAIL,
                    admin_emails
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                message = "Your edit has been sent for admin approval."
               

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': message,
                    'redirect_url': reverse('veterinary:event_detail', args=[event.pk])
                })

           
            return redirect('veterinary:event_detail', pk=event.pk)

        # Return AJAX errors
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = {f: [str(e) for e in err] for f, err in form.errors.items()}
            return JsonResponse({'status': 'error', 'errors': errors})

        messages.error(request, "Error updating event.")

    else:
        form = EventForm(instance=event, user=request.user, edit_mode=True)

    return render(request, 'vet/event_form.html', {
        'form': form,
        'edit_mode': True,
        'event': event,
      

        # Piggery
        'initial_line': initial_line,
        'initial_block': initial_block,
        'initial_pen': initial_pen,

        # Paddock + Ruminant
        'initial_paddock': initial_paddock,
        'initial_small_ruminant': initial_small_ruminant,

        #Piggery
        'is_vet_piggery': request.user.profile.is_vet_piggery,
    })


# @login_required
# @require_POST
# def retract_event_edit(request, edit_id):
#     # Fetch the pending edit belonging to the user
#     pending_edit = get_object_or_404(PendingEventEdit, id=edit_id, submitted_by=request.user)

#     # Store the ID before deleting
#     request_id = f"SKAAL-EVT-{pending_edit.id}"
#     event_name = pending_edit.event.event_name

#     if pending_edit.status != 'pending':
#         messages.error(request, "This request has already been processed.")
#         return redirect('veterinary:vet_index')

#     # Notify Admins
#     admin_emails = [u.email for u in User.objects.filter(is_staff=True, is_active=True) if u.email]
#     if admin_emails:
#         subject = f"[{request_id}] Event Edit Retracted by {request.user.get_full_name()}"
#         message = f"The edit request for event '{pending_edit.event.event_name}' was retracted by the vet."
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails)

#     # Delete the record
#     pending_edit.delete()

#     messages.success(request, "The edit request has been retracted.")
#     return redirect('veterinary:vet_index')

@login_required
@require_POST
def retract_event_edit(request, edit_id):
    # Fetch the pending edit belonging to the user
    pending_edit = get_object_or_404(PendingEventEdit, id=edit_id, submitted_by=request.user)

    if pending_edit.status != 'pending':
        messages.error(request, "This request has already been processed.")
        return redirect('veterinary:vet_index')

    # Capture the context input from POST (without saving to the model)
    reason = request.POST.get('retraction_reason', '').strip()
    reason_str = reason if reason else "No reason provided."

    # Store the ID before deleting
    request_id = f"SKAAL-EVT-{pending_edit.id}"

    # Notify Admins
    admin_emails = [u.email for u in User.objects.filter(is_staff=True, is_active=True) if u.email]
    if admin_emails:
        subject = f"[{request_id}] Event Edit Retracted by {request.user.get_full_name()}"
        message = (
            f"The edit request for event '{pending_edit.event.event_name}' was retracted by the vet.\n\n"
            f"Reason for Retraction:\n{reason_str}"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails)

    # Delete the record
    pending_edit.delete()

    messages.success(request, "The edit request has been retracted.")
    return redirect('veterinary:vet_index')

@login_required
def delete_event(request, pk):
    event = get_object_or_404(EventType, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('veterinary:event_records')
    return redirect('veterinary:event_detail', pk=pk)


# @login_required
# def retract_census_edit(request, queue_id):
#     queue_item = get_object_or_404(CensusApprovalQueue, id=queue_id, requested_by=request.user)

#     # Store identifier before deleting the object
#     request_id = f"SKAAL-CEN-{queue_item.id}"
#     census = queue_item.census

#     if queue_item.is_processed:
#         messages.error(request, "Cannot retract a request that has already been processed.")
#         return redirect('veterinary:vet_index')

#     census = queue_item.census
    
#     # Notify admins
#     subject = f"[{request_id}] Census Edit Retracted by {request.user.get_full_name()}"
#     text_content = f"The edit request for Census #{census.pk} was retracted by the vet."
#     admin_emails = [u.email for u in User.objects.filter(profile__is_boss=True, is_active=True) if u.email]
    
#     if admin_emails:
#         send_mail(subject, text_content, settings.DEFAULT_FROM_EMAIL, admin_emails)

#     # Unlock the census and remove the queue item
#     census.is_pending_review = False
#     census.save()
#     queue_item.delete()

#     messages.success(request, "Your edit request has been retracted successfully.")
#     return redirect('veterinary:vet_index')

@login_required
@require_POST
def retract_census_edit(request, queue_id):
    queue_item = get_object_or_404(CensusApprovalQueue, id=queue_id, requested_by=request.user)

    if queue_item.is_processed:
        messages.error(request, "Cannot retract a request that has already been processed.")
        return redirect('veterinary:vet_index')

    # Capture the context input from POST (without saving to the model)
    reason = request.POST.get('retraction_reason', '').strip()
    reason_str = reason if reason else "No reason provided."

    # Store identifier before deleting the object
    request_id = f"SKAAL-CEN-{queue_item.id}"
    census = queue_item.census
    
    # Notify admins
    subject = f"[{request_id}] Census Edit Retracted by {request.user.get_full_name()}"
    text_content = (
        f"The edit request for Census #{census.pk} was retracted by the vet.\n\n"
        f"Reason for Retraction:\n{reason_str}"
    )
    admin_emails = [u.email for u in User.objects.filter(profile__is_boss=True, is_active=True) if u.email]
    
    if admin_emails:
        send_mail(subject, text_content, settings.DEFAULT_FROM_EMAIL, admin_emails)

    # Unlock the census and remove the queue item
    census.is_pending_review = False
    census.save()
    queue_item.delete()

    messages.success(request, "Your edit request has been retracted successfully.")
    return redirect('veterinary:vet_index')