from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, CensusForm, CensusRecordFormSet
from drugapp.models import Dispatch, Drug, InventoryLog
from django.utils.timezone import localtime, now, localdate, timedelta
from django.db.models import Q, Prefetch, Max
from itertools import chain
from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from farmrecord.models import EventType, Census, Animals, PendingEventEdit, AnimalType, CensusRecord
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
    status = request.GET.get("status", "pending")

    # Pending edits
    pending_edits = PendingEventEdit.objects.filter(
        submitted_by=request.user,
        status=status
    ).select_related(
        "event", "event__animal", "event__animal_type", "reviewed_by"
    )

    # pending_edits = PendingEventEdit.objects.filter(
    #     submitted_by=request.user,
    #     status='pending'
    # ).select_related(
    #     "event", "event__animal", "event__animal_type"
    # )

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
        'current_status': status,
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
        'entered_at': d.entered_at.strftime('%Y-%m-%d %H:%M'),
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

    return render(request, 'vet/event_form.html', {'form': form, 'is_vet_piggery': request.user.profile.is_vet_piggery,})


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
            event_types = ['mortality', 'culling', 'farrowing', 'sale', 'procurement']

        elif profile.is_vet_paddock:
            events = events.filter(animal__animal_name='cattle')
            event_types = ['mortality', 'calving', 'farrowing', 'sale', 'procurement']

        elif profile.is_vet_smallruminant:
            events = events.filter(animal__animal_name__in=['sheep', 'goat'])
            event_types = ['mortality', 'culling', 'lambing', 'kidding', 'sale', 'procurement']

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

    events = events.order_by('-created_at')

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


@login_required
def event_detail(request, pk):
  event = get_object_or_404(EventType.objects.select_related('animal', 'animal_type'), pk=pk)

  context = {
    'event': event
  }
  return render(request, 'vet/event_details.html', context)


@login_required
def create_census(request):
    user = request.user

    if request.method == 'POST':
        form = CensusForm(request.POST, user=user)
        formset = CensusRecordFormSet(request.POST, user=user)

        if form.is_valid() and formset.is_valid():
            census = form.save(commit=False)
            census.save()
            records = formset.save(commit=False)
            for record in records:
                record.census = census
                record.save()
            census.update_total()
            messages.success(request, "Census record created successfully.")
            return redirect('veterinary:census_records')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CensusForm(user=user)
        formset = CensusRecordFormSet(user=user)

    return render(request, 'vet/census_form.html', {'form': form, 'formset': formset})



@login_required
def census_records(request):
    """Display census records for the logged-in vet's section with date filters and no duplicates."""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page = request.GET.get('page', 1)

    censuses = (
        Census.objects
        .select_related('animal')
        .prefetch_related('records', 'records__animal_type')  # separate prefetch levels
        .order_by('-census_date')
    )

    vet_profile = request.user.profile

    if vet_profile.is_vet_piggery:
        censuses = censuses.filter(animal__animal_name__iexact='pig')
    elif vet_profile.is_vet_paddock:
        censuses = censuses.filter(animal__animal_name__iexact='cattle')
    elif vet_profile.is_vet_smallruminant:
        censuses = censuses.filter(animal__animal_name__in=['sheep', 'goat'])
    elif not vet_profile.is_vet:
        censuses = Census.objects.none()

    # Date range filter
    # Date range filter
    if start_date:
        censuses = censuses.filter(census_date__gte=parse_date(start_date))
    if end_date:
        end = parse_date(end_date)
        if end:
            censuses = censuses.filter(census_date__lt=end + timedelta(days=1))
    # if start_date:
    #     censuses = censuses.filter(census_date__gte=parse_date(start_date))
    # if end_date:
    #     censuses = censuses.filter(census_date__lte=parse_date(end_date))

    # Ensure uniqueness
    censuses = censuses.distinct()

    paginator = Paginator(censuses, 5)
    page_obj = paginator.get_page(page)

    # AJAX infinite scroll
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('vet/census_records_list.html', {'censuses': page_obj})
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    return render(request, 'vet/census_records.html', {
        'censuses': page_obj,
        'start_date': start_date,
        'end_date': end_date,
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

                    # if hasattr(value, 'pk'):
                    #     pending_data[key] = {
                    #         "id": value.pk,
                    #         "label": str(value)
                    #     }
                    # else:
                    #     pending_data[key] = value
                # pending_data = {}
                # for key, value in form.cleaned_data.items():
                #     if key == 'edit_note':
                #         continue
                #     pending_data[key] = value.pk if hasattr(value, 'pk') else value

                pending = PendingEventEdit.objects.create(
                    event=event,
                    submitted_by=request.user,
                    data=pending_data,
                    vet_note=form.cleaned_data.get('edit_note', '')
                )
                subject = "New Event Edit Pending Approval"
                context = {
                    'event': event,
                    'user': request.user,
                    'data': pending_data,
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

            messages.success(request, message)
            return redirect('veterinary:event_detail', pk=event.pk)

        # Return AJAX errors
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            errors = {f: [str(e) for e in err] for f, err in form.errors.items()}
            return JsonResponse({'status': 'error', 'errors': errors})

        messages.error(request, "Error updating event.")

    else:
        form = EventForm(instance=event, user=request.user)

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


@login_required
def delete_event(request, pk):
    event = get_object_or_404(EventType, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('veterinary:event_records')
    return redirect('veterinary:event_detail', pk=pk)
