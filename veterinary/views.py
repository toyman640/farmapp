from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, CensusForm, CensusRecordFormSet, PiggeryCensusRecordFormSet
from drugapp.models import Dispatch, Drug, InventoryLog
from django.utils.timezone import localtime, now, localdate, timedelta
from django.db.models import Q, Prefetch, Max, Sum, Case, When, F, IntegerField
from itertools import chain, zip_longest
from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from farmrecord.models import EventType, Census, Animals, PendingEventEdit, AnimalType, CensusRecord, CensusApprovalQueue, PiggeryCensusRecord, PiggeryLine, CensusProjection
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.template.loader import render_to_string
import datetime
from datetime import timedelta, datetime
import json
from django.forms.models import model_to_dict
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from itertools import zip_longest
from main.services import run_projection_calculation

User = get_user_model()
# Create your views here.

# @login_required
# def vet_index(request):
#     today = localdate()
#     now_time = now()
#     last_24_hours = now_time - timedelta(hours=24)

#     today_dispatches = Dispatch.objects.filter(dispatched_at__date=today)
#     new_drugs = Drug.objects.filter(entered_at__gte=last_24_hours)
#     restocked_logs = InventoryLog.objects.filter(
#         updated_at__gte=last_24_hours,
#         new_quantity__gt=F('previous_quantity')
#     ).select_related('drug')
#     restocked_drugs = Drug.objects.filter(id__in=restocked_logs.values_list('drug_id', flat=True))
#     combined_new_drugs = list(set(chain(new_drugs, restocked_drugs)))
#     # status = request.GET.get("status", "pending")
#     # Get status filters independently
#     event_status = request.GET.get("event_status", "pending")
#     census_status = request.GET.get("census_status", "pending")

#     # Pending edits
#     pending_edits = PendingEventEdit.objects.filter(
#         submitted_by=request.user,
#         status=event_status
#     ).select_related(
#         "event", "event__animal", "event__animal_type", "reviewed_by"
#     )


#     for p in pending_edits:
#         animal_id = p.data.get("animal")
#         if animal_id:
#             try:
#                 p.data["animal_obj"] = Animals.objects.get(id=animal_id)
#             except Animals.DoesNotExist:
#                 p.data["animal_obj"] = None

#         animal_type_id = p.data.get("animal_type")
#         if animal_type_id:
#             try:
#                 p.data["animal_type_obj"] = AnimalType.objects.get(id=animal_type_id)
#             except AnimalType.DoesNotExist:
#                 p.data["animal_type_obj"] = None

#     # 2. Fetch Census Changes based on current status filter
#     is_processed_map = {
#         "pending": False,
#         "approved": True,
#         "rejected": True
#     }
#     is_processed_val = is_processed_map.get(census_status, False)

#     # 1. Start with the base query
#     census_queries = CensusApprovalQueue.objects.filter(requested_by=request.user).select_related('census', 'census__animal')

#     # 2. Filter based on status
#     if census_status == "pending":
#         census_queries = census_queries.filter(is_processed=False)
#     elif census_status == "approved":
#         census_queries = census_queries.filter(is_processed=True, approved=True)
#     elif census_status == "rejected":
#         census_queries = census_queries.filter(is_processed=True, approved=False)

#     # 3. Add select_related
#     census_queries = census_queries.select_related('census', 'census__animal')
    


#     if census_status in ["approved", "rejected"]:
#         approved_bool = True if census_status == "approved" else False
#         census_queries = census_queries.filter(approved=approved_bool)

#     # Hydrate JSON payloads with readable DB items for the template
#     census_edits = []
#     for queue_item in census_queries:
#         payload = queue_item.form_data_payload or {}
#         records_payload = payload.get('records', [])
        
#         # FIX: Check if this is a Piggery census to use the correct related name
#         is_piggery = queue_item.census.animal.animal_name.lower() == 'pig'
        
#         if is_piggery:
#             # Use piggery_records instead of records
#             db_records = {
#                 r.line_id: r.number # Adjust to match your model fields
#                 for r in queue_item.census.piggery_records.all()
#             }
#         else:
#             # Standard records
#             db_records = {
#                 r.animal_type_id: r.number_of_animals 
#                 for r in queue_item.census.records.all()
#             }

#         processed_records = []
#         for item in records_payload:
#             # If piggery, we look up PiggeryLine, otherwise AnimalType
#             if is_piggery:
#                 line_id = item.get('line')
#                 try:
#                     line_obj = PiggeryLine.objects.get(id=line_id)
#                     type_name = str(line_obj)
#                 except PiggeryLine.DoesNotExist:
#                     type_name = "Unknown Line"
#                 old_count = db_records.get(int(line_id) if line_id else 0, 0)
#                 new_count = item.get('number', 0)
#             else:
#                 type_id = item.get('animal_type')
#                 try:
#                     type_obj = AnimalType.objects.get(id=type_id)
#                     type_name = type_obj.animal_type_name
#                 except AnimalType.DoesNotExist:
#                     type_name = "Unknown Type"
#                 old_count = db_records.get(type_id, 0)
#                 new_count = item.get('number_of_animals', 0)

#             processed_records.append({
#                 'animal_type_name': type_name,
#                 'new_count': new_count,
#                 'old_count': old_count,
#                 'is_deleted': item.get('DELETE', False)
#             })
        

#         census_edits.append({
#             'queue_obj': queue_item,
#             'census': queue_item.census,
#             'main_form': payload.get('main_form', {}),
#             'records': processed_records,
#             'status': census_status
#         })

#     # -------------------- Latest census per animal --------------------
#     profile = getattr(request.user, "profile", None)

#     # Determine the vet section
#     if profile.is_vet_piggery:
#         animals_for_section = Animals.objects.filter(animal_name__iexact='pig')
#     elif profile.is_vet_paddock:
#         animals_for_section = Animals.objects.filter(animal_name__iexact='cattle')
#     elif profile.is_vet_smallruminant:
#         animals_for_section = Animals.objects.filter(animal_name__in=['sheep','goat'])
#     else:
#         animals_for_section = Animals.objects.none()

#     # Get the latest census per animal
#     census_list = []
#     for animal in animals_for_section:
#         last_census = Census.objects.filter(animal=animal).order_by('-census_date').first()
        
#         if last_census:
#             # Apply annotation only for Piggery
#             if animal.animal_name.lower() == 'pig':
#                 last_census = Census.objects.filter(id=last_census.id).annotate(
#                     sum_adults=Sum(
#                         Case(
#                             When(piggery_records__line__name__icontains='goose', then=0),
#                             When(piggery_records__line__name__icontains='crocodile', then=0),
#                             default=F('piggery_records__number'),
#                             output_field=IntegerField()
#                         )
#                     ),
#                     sum_piglets=Sum('piggery_records__total_piglets')
#                 ).first()
#                 # Create a dynamic attribute for the template
#                 last_census.calculated_total = (last_census.sum_adults or 0) + (last_census.sum_piglets or 0)
#             else:
#                 last_census.calculated_total = last_census.total_animals
            
#             census_list.append(last_census)

#     context = {
#         'today_dispatches': today_dispatches,
#         'today_date': today,
#         'recent_drugs': combined_new_drugs,
#         'event_edits': pending_edits,
#         'census_edits': census_edits,
#         # 'current_status': status,
#         'current_event_status': event_status,
#         'current_census_status': census_status,
#         'census_list': census_list,
#     }

#     return render(request, 'vet/index.html', context)

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

    # -------------------- EVENT RECORDS FILTERING (Latest Date by Default + Date Picker) --------------------
    selected_date_str = request.GET.get("event_date")
    
    # Assuming your main event model is named `Event` (adjust if your model name differs, e.g., LivestockEvent)
    if selected_date_str:
        try:
            target_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            target_date = today
    else:
        # Default behavior: Find the latest date that has event records
        latest_event = EventType.objects.order_by('-event_date', '-created_at').first()
        target_date = latest_event.event_date if latest_event else today
    # Fetch all events matching the target date
    filtered_events = EventType.objects.filter(event_date=target_date) # Adjust field name like event_date if necessary
    summarized_events = (
        EventType.objects.filter(event_date=target_date)
        .values('event_name')
        .annotate(total_count=Sum('number_of_animals'))
        .order_by('event_name')
    )
    # --------------------------------------------------------------------------------------------------------

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
        
        is_piggery = queue_item.census.animal.animal_name.lower() == 'pig'
        
        if is_piggery:
            db_records = {
                r.line_id: r.number 
                for r in queue_item.census.piggery_records.all()
            }
        else:
            db_records = {
                r.animal_type_id: r.number_of_animals 
                for r in queue_item.census.records.all()
            }

        processed_records = []
        for item in records_payload:
            if is_piggery:
                line_id = item.get('line')
                try:
                    line_obj = PiggeryLine.objects.get(id=line_id)
                    type_name = str(line_obj)
                except PiggeryLine.DoesNotExist:
                    type_name = "Unknown Line"
                old_count = db_records.get(int(line_id) if line_id else 0, 0)
                new_count = item.get('number', 0)
            else:
                type_id = item.get('animal_type')
                try:
                    type_obj = AnimalType.objects.get(id=type_id)
                    type_name = type_obj.animal_type_name
                except AnimalType.DoesNotExist:
                    type_name = "Unknown Type"
                old_count = db_records.get(type_id, 0)
                new_count = item.get('number_of_animals', 0)

            processed_records.append({
                'animal_type_name': type_name,
                'new_count': new_count,
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

    if profile.is_vet_piggery:
        animals_for_section = Animals.objects.filter(animal_name__iexact='pig')
    elif profile.is_vet_paddock:
        animals_for_section = Animals.objects.filter(animal_name__iexact='cattle')
    elif profile.is_vet_smallruminant:
        animals_for_section = Animals.objects.filter(animal_name__in=['sheep','goat'])
    else:
        animals_for_section = Animals.objects.none()

    census_list = []
    for animal in animals_for_section:
        last_census = Census.objects.filter(animal=animal).order_by('-census_date').first()
        
        if last_census:
            if animal.animal_name.lower() == 'pig':
                last_census = Census.objects.filter(id=last_census.id).annotate(
                    sum_adults=Sum(
                        Case(
                            When(piggery_records__line__name__icontains='goose', then=0),
                            When(piggery_records__line__name__icontains='crocodile', then=0),
                            default=F('piggery_records__number'),
                            output_field=IntegerField()
                        )
                    ),
                    sum_piglets=Sum('piggery_records__total_piglets')
                ).first()
                last_census.calculated_total = (last_census.sum_adults or 0) + (last_census.sum_piglets or 0)
            else:
                last_census.calculated_total = last_census.total_animals
            
            census_list.append(last_census)
    
    # -------------------- CENSUS CHART DATA --------------------
    census_filter_type = request.GET.get("census_filter", "progressive") # 'progressive' or 'monthly'
    
    chart_labels = []
    chart_datasets = []

    for animal in animals_for_section:
        animal_name_lower = animal.animal_name.lower()
        census_qs = Census.objects.filter(animal=animal).order_by('census_date')

        if animal_name_lower == 'pig':
            # Monthly projection: filter to only the last record of each month if requested
            if census_filter_type == 'monthly':
                # Group by year and month, taking the max census_date per month
                from django.db.models.functions import ExtractYear, ExtractMonth
                monthly_dates = (
                    census_qs.annotate(year=ExtractYear('census_date'), month=ExtractMonth('census_date'))
                    .values('year', 'month')
                    .annotate(max_date=Max('census_date'))
                    .values_list('max_date', flat=True)
                )
                census_qs = census_qs.filter(census_date__in=monthly_dates).order_by('census_date')

            # Prepare data points for Piggery (Separating General/Adults vs Piglets, excluding geese & crocodiles)
            general_data = []
            piglet_data = []
            dates_list = []

            for c in census_qs:
                dates_list.append(c.census_date.strftime('%Y-%m-%d'))
                
                # Annotate/Calculate sums excluding geese and crocodiles for general, and sum piglets
                annotated_c = Census.objects.filter(id=c.id).annotate(
                    sum_adults=Sum(
                        Case(
                            When(piggery_records__line__name__icontains='goose', then=0),
                            When(piggery_records__line__name__icontains='crocodile', then=0),
                            default=F('piggery_records__number'),
                            output_field=IntegerField()
                        )
                    ),
                    sum_piglets=Sum('piggery_records__total_piglets')
                ).first()

                general_data.append(annotated_c.sum_adults or 0)
                piglet_data.append(annotated_c.sum_piglets or 0)

            chart_labels = dates_list # shared X-axis dates
            chart_datasets = [
                {'label': 'General', 'data': general_data, 'backgroundColor': 'rgba(78, 115, 223, 0.7)', 'borderColor': '#4e73df', 'borderWidth': 1},
                {'label': 'Piglets', 'data': piglet_data, 'backgroundColor': 'rgba(28, 200, 138, 0.7)', 'borderColor': '#1cc88a', 'borderWidth': 1}
            ]
        else:
            # Other sections (Cattle, Sheep, Goat - Progressive records entered monthly)
            totals_data = []
            dates_list = []
            for c in census_qs:
                dates_list.append(c.census_date.strftime('%Y-%m-%d'))
                totals_data.append(c.total_animals or 0)

            chart_labels = dates_list
            chart_datasets = [
                {'label': f'{animal.animal_name.title()} (Total)', 'data': totals_data, 'backgroundColor': 'rgba(28, 200, 138, 0.7)', 'borderColor': '#1cc88a', 'borderWidth': 1}
            ]

    today = localdate()
    user_profile = request.user.profile
    
    # 1. Base queryset filtered by user role/section
    events_qs = EventType.objects.all()
    if user_profile.is_vet_piggery:
        events_qs = events_qs.filter(animal__animal_name__iexact='pig')
    elif user_profile.is_vet_paddock:
        events_qs = events_qs.filter(animal__animal_name__iexact='cattle')
    elif user_profile.is_vet_smallruminant:
        events_qs = events_qs.filter(animal__animal_name__in=['sheep', 'goat'])

    selected_date_str = request.GET.get("event_date")
    
    # 2. Determine target date for initial load
    if selected_date_str:
        try:
            target_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            target_date = today
    else:
        # Find the absolute latest event date for THIS specific section
        latest_event = events_qs.order_by('-event_date', '-created_at').first()
        target_date = latest_event.event_date if latest_event else today

    # 3. Fetch summarized events for that date
    summarized_events = (
        events_qs.filter(event_date=target_date)
        .values('event_name')
        .annotate(total_count=Sum('number_of_animals'))
        .order_by('event_name')
    )

    context = {
        'today_dispatches': today_dispatches,
        'today_date': today,
        'recent_drugs': combined_new_drugs,
        'event_edits': pending_edits,
        'census_edits': census_edits,
        'current_event_status': event_status,
        'current_census_status': census_status,
        'census_list': census_list,
        'summarized_events': summarized_events,
        'selected_event_date': target_date,
        'chart_labels': chart_labels,
        'chart_datasets': chart_datasets,
        'is_piggery_section': profile.is_vet_piggery,
        'current_census_filter': census_filter_type,
    }
    return render(request, 'vet/index.html', context)


# @login_required
# def load_event_records_ajax(request):
#     selected_date_str = request.GET.get("event_date")
#     today = localdate()
    
#     if selected_date_str:
#         try:
#             target_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
#         except ValueError:
#             target_date = today
#     else:
#         # Default behavior: Find the latest date that has event records
#         latest_event = EventType.objects.order_by('-event_date', '-created_at').first()
#         target_date = latest_event.event_date if latest_event else today

#     summarized_events = (
#         EventType.objects.filter(event_date=target_date)
#         .values('event_name')
#         .annotate(total_count=Sum('number_of_animals'))
#         .order_by('event_name')
#     )

#     context = {
#         'summarized_events': summarized_events,
#         'selected_event_date': target_date,
#     }
    
#     # Render just the inner card content or the wrapper fragment
#     html_content = render_to_string('vet/partials/event_records_card.html', context, request=request)
#     return JsonResponse({'html': html_content})

@login_required
def load_event_records_ajax(request):
    selected_date_str = request.GET.get("event_date")
    today = localdate()
    
    user_profile = request.user.profile  # Using your Userp model linked via OneToOneField
    
    # 1. Base queryset filtered by user role/section
    events_qs = EventType.objects.all()
    if user_profile.is_vet_piggery:
        events_qs = events_qs.filter(animal__animal_name__iexact='pig')
    elif user_profile.is_vet_paddock:
        events_qs = events_qs.filter(animal__animal_name__iexact='cattle')
    elif user_profile.is_vet_smallruminant:
        events_qs = events_qs.filter(animal__animal_name__in=['sheep', 'goat'])

    # 2. Determine target date
    if selected_date_str:
        try:
            target_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            target_date = today
    else:
        # Default behavior: Find the absolute latest event date for THIS specific section only
        latest_event = events_qs.order_by('-event_date', '-created_at').first()
        # If records exist, use that latest date. Otherwise, fall back to today.
        target_date = latest_event.event_date if latest_event else today

    # 3. Fetch and summate events matching the target date AND the user's role
    summarized_events = (
        events_qs.filter(event_date=target_date)
        .values('event_name')
        .annotate(total_count=Sum('number_of_animals'))
        .order_by('event_name')
    )
    
    context = {
        'summarized_events': summarized_events,
        'selected_event_date': target_date,
    }
    
    html_content = render_to_string('vet/partials/event_records_card.html', context, request=request)
    return JsonResponse({'html': html_content})

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
        # if getattr(request.user.profile, 'is_vet_piggery', False):
        #     line = request.POST.get('lineSelect', '')
            
        #     block = request.POST.get('blockSelect', '')
        #     pen = request.POST.get('penSelect', '')
        #     post_data['location'] = " ".join(filter(None, [line, block, pen]))
        #     # event.location = " ".join(filter(None, [line, block, pen]))
        # # form = EventForm(request.POST, request.FILES, user=request.user)
        # # form = EventForm(post_data, request.FILES, user=request.user)
        event_name = post_data.get('event_name', '').lower()
        is_piggery = getattr(request.user.profile, 'is_vet_piggery', False)
        
        # Validation Logic
        error_message = None
        
        if is_piggery:
            # Piggery Rules: Castration allows blank pen, others require full string
            if event_name != 'castration':
                if not (request.POST.get('lineSelect') and request.POST.get('blockSelect') and request.POST.get('penSelect')):
                    error_message = "Line, Block, and Pen are required for this event."
            else:
                if not (request.POST.get('lineSelect') and request.POST.get('blockSelect')):
                    error_message = "Line and Block are required for castration."
        else:
            # Other sections: Location is mandatory
            if not post_data.get('location'):
                error_message = "Location is required for this record."

        if error_message:
            return JsonResponse({'status': 'error', 'message': error_message}, status=400)

        form = EventForm(post_data, request.FILES, user=request.user, edit_mode=False)

        
        
        if form.is_valid():
            # event = form.save(commit=False)

            instance = form.save(commit=False)
            instance.logged_by = request.user
            instance.save()


            # event.save()
            # event = form.save()

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
            else:
                # ADD THIS: Manual check to catch the missing location error for non-castration
                event_name = request.POST.get('event_name', '').lower()
                line = request.POST.get('lineSelect', '')
                block = request.POST.get('blockSelect', '')
                pen = request.POST.get('penSelect', '')

                if event_name != 'castration' and not pen:
                    form.add_error('location', 'Location (including Pen) is required for this event.')

                # Then proceed to collect and return errors
                errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}

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
    paginator = Paginator(events, 10)
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
    # if vet_profile.is_vet_piggery:
    #     censuses = censuses.filter(animal__animal_name__iexact='pig').annotate(
    #         sum_adults=Sum('piggery_records__number'),
    #         sum_piglets=Sum('piggery_records__total_piglets')
    #     ).prefetch_related(
    #         Prefetch('piggery_records', queryset=PiggeryCensusRecord.objects.select_related('line'))
    #     )
        
    # Inside your view, update the piggery filter block:
    # Inside your piggery_census_records_admin view logic:
    if vet_profile.is_vet_piggery:
        censuses = censuses.filter(animal__animal_name__iexact='pig').annotate(
            # General = Records excluding Crocodile and Goose
            sum_adults=Sum(
                Case(
                    When(piggery_records__line__name__icontains='goose', then=0),
                    When(piggery_records__line__name__icontains='crocodile', then=0),
                    default=F('piggery_records__number'),
                    output_field=IntegerField()
                )
            ),
            sum_piglets=Sum('piggery_records__total_piglets'),
            sum_geese=Sum(
                Case(When(piggery_records__line__name__icontains='goose', then=F('piggery_records__number')), default=0, output_field=IntegerField())
            ),
            sum_crocodiles=Sum(
                Case(When(piggery_records__line__name__icontains='crocodile', then=F('piggery_records__number')), default=0, output_field=IntegerField())
            )
        ).annotate(
            # Grand Total = sum_adults (which already excludes croc/goose) + sum_piglets
            grand_total=F('sum_adults') + F('sum_piglets')
        ).prefetch_related(
            Prefetch('piggery_records', queryset=PiggeryCensusRecord.objects.select_related('line'))
        )
    elif vet_profile.is_vet_paddock:
        censuses = censuses.filter(animal__animal_name__iexact='cattle').prefetch_related(
            Prefetch('records', queryset=CensusRecord.objects.select_related('animal_type'))
        )
    elif vet_profile.is_vet_smallruminant:
        censuses = censuses.filter(animal__animal_name__iexact='sheep').prefetch_related(
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

    paginator = Paginator(censuses, 10)
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
            # 1. Save form with commit=False to get the instance
            census = form.save(commit=False)
            
            # 2. Assign the user
            census.logged_by = request.user
            
            # 3. Save to the database
            census.save()

            
            
            # 4. Save formset records
            records = formset.save(commit=False)
            for record in records:
                record.census = census
                record.save()
            census.update_total()

            # 4. Now run projection calculation using the PREVIOUS census
            # We exclude the current census to find the most recent one before this
            last_census = Census.objects.filter(animal=census.animal)\
                                        .exclude(id=census.id)\
                                        .order_by('-census_date').first()

            if last_census:
                # Determine start_count for the projection
                if census.animal.animal_name.lower() == 'pig':
                    # Exclude exotic lines as we did in your dashboard
                    piggery_data = PiggeryCensusRecord.objects.filter(census=last_census)\
                        .exclude(line__name__icontains='croc')\
                        .exclude(line__name__icontains='goose')\
                        .aggregate(gen=Sum('number'), pig=Sum('total_piglets'))
                    start_count = (piggery_data['gen'] or 0) + (piggery_data['pig'] or 0)
                else:
                    start_count = last_census.total_animals

                # # data = run_projection_calculation(census.animal, last_census.census_date, start_count)
                # data = run_projection_calculation(
                #     census.animal, 
                #     last_census.census_date, 
                #     start_count, 
                #     end_date=census.census_date # Lock the projection to the day of the census
                # )

                # STRICT CALL: 
                # Start = Last Census Date, End = New Census Date
                data = run_projection_calculation(
                    animal_obj=census.animal, 
                    start_date=last_census.census_date, 
                    end_date=census.census_date, 
                    start_count=start_count
                )

                # 5. Create Projection record
                CensusProjection.objects.create(
                    census=census,
                    start_count=data['start_count'],
                    projected_count=data['projected_count'],
                    total_mortality=data['total_mortality'],
                    total_culling=data['total_culling'],
                    total_sale=data['total_sale'],
                    total_gift=data['total_gift'],
                    total_births=data['total_births'],
                    total_procurement=data['total_procurement']
                )
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


# @login_required
# def edit_census(request, pk):
#     user = request.user
#     census = get_object_or_404(Census, pk=pk)
    
#     # 1. Determine if this is a Piggery census
#     is_piggery = getattr(user.profile, 'is_vet_piggery', False)
#     FormSetClass = PiggeryCensusRecordFormSet if is_piggery else CensusRecordFormSet
    
#     # 2. Lock check logic
#     if census.is_pending_review:
#         if CensusApprovalQueue.objects.filter(census=census, is_processed=False).exists():
#             messages.error(request, "This census record is currently locked pending admin approval.")
#             return redirect('veterinary:census_records')
#         else:
#             census.is_pending_review = False
#             census.save()

#     if request.method == 'POST':
#         form = CensusForm(request.POST, instance=census, user=user)
#         formset = FormSetClass(request.POST, instance=census, user=user, prefix='records')

#         if form.is_valid() and formset.is_valid():
#             user_note = request.POST.get('request_note', '').strip()
            
#             # 3. Dynamic Payload Construction
#             records_data = []
#             for f in formset.forms:
#                 if f.has_changed() or f.cleaned_data.get('id'):
#                     record_dict = {'DELETE': f.cleaned_data.get('DELETE', False)}
                    
#                     if is_piggery:
#                         record_dict.update({
#                             'id': f.cleaned_data.get('id').id if f.cleaned_data.get('id') else None,
#                             'line': f.cleaned_data['line'].id,
#                             'number': f.cleaned_data['number'],
#                             'piglets': f.cleaned_data.get('piglets', 0), # Capture this
#                             'note': f.cleaned_data['note']
#                         })
#                     else:
#                         record_dict.update({
#                             'id': f.cleaned_data.get('id').id if f.cleaned_data.get('id') else None,
#                             'animal_type': f.cleaned_data['animal_type'].id,
#                             'number_of_animals': f.cleaned_data['number_of_animals']
#                         })
#                     records_data.append(record_dict)

#             serialized_payload = {
#                 'main_form': {
#                     'census_date': form.cleaned_data['census_date'].isoformat(),
#                     'notes': form.cleaned_data['notes'],
#                 },
#                 'records': records_data
#             }

#             # 4. Save to Queue
#             queue_item = CensusApprovalQueue.objects.create(
#                 census=census,
#                 requested_by=user,
#                 form_data_payload=serialized_payload,
#                 request_note=user_note
#             )

#             # 5. Lock and Notify
#             census.is_pending_review = True
#             census.save()
#             request_id = f"SKAAL-CEN-{queue_item.id}"

#             # Prepare email context
#             # Note: You can add a similar check here to format Piggery records for the email
#             subject = f"[{request_id}] New Census Edit Pending Approval"
#             context = {
#                 'vet_name': user.get_full_name(),
#                 'census_id': census.pk,
#                 'review_url': request.build_absolute_uri(reverse('veterinary:vet_index')),
#                 'user_note': user_note,
#             }

#             html_content = render_to_string('emails/census_edit_status.html', context)
#             admin_emails = [u.email for u in User.objects.filter(profile__is_boss=True, is_active=True) if u.email]

#             if admin_emails:
#                 email = EmailMultiAlternatives(subject, f"New edit for #{census.pk}", settings.DEFAULT_FROM_EMAIL, admin_emails)
#                 email.attach_alternative(html_content, "text/html")
#                 email.send()

#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({'status': 'success', 'message': 'Your updates have been submitted to the administrator for verification.'})
            
#             messages.success(request, "Your updates have been submitted to the administrator for verification.")
#             return redirect('veterinary:vet_index')

#     else:
#         form = CensusForm(instance=census, user=user)
#         formset = FormSetClass(instance=census, user=user, prefix='records')

#     return render(request, 'vet/census_form.html', {
#         'form': form,
#         'formset': formset,
#         'is_edit': True,
#         'census': census,
#     })


@login_required
def edit_census(request, pk):
    user = request.user
    census = get_object_or_404(Census, pk=pk)
    is_piggery = getattr(user.profile, 'is_vet_piggery', False)
    FormSetClass = PiggeryCensusRecordFormSet if is_piggery else CensusRecordFormSet

    # Prepare existing records for the JS
    existing_records = []
    if is_piggery:
        for r in census.piggery_records.all():
            existing_records.append({
                'id': r.id,
                'typeId': r.line.id,
                'typeText': str(r.line),
                'count': r.number,
                'piglets': r.total_piglets,
                'note': r.note
            })
    else:
        for r in census.records.all():
            existing_records.append({
                'id': r.id,
                'typeId': r.animal_type.id,
                'typeText': r.animal_type.animal_type_name,
                'count': r.number_of_animals
            })

    # Lock check logic
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
            try:
                # 3. Dynamic Payload Construction
                records_data = []
                for f in formset.forms:
                    if f.has_changed() or f.cleaned_data.get('id'):

                        # Check specifically for the delete flag from the formset
                        is_deleted = f.cleaned_data.get('DELETE', False)
                        record_dict = {'DELETE': is_deleted}
                        if not is_deleted:
                            if is_piggery:
                                record_dict.update({
                                    'id': f.cleaned_data.get('id').id if f.cleaned_data.get('id') else None,
                                    'line': f.cleaned_data['line'].id,
                                    'number': f.cleaned_data['number'],
                                    'piglets': f.cleaned_data.get('total_piglets', 0),
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
                    request_note=request.POST.get('request_note', '').strip()
                )

                # 5. Lock and Notify
                census.is_pending_review = True
                census.save()

                admin_emails = list(User.objects.filter(profile__is_boss=True, is_active=True).values_list('email', flat=True))
                if not admin_emails:
                    return JsonResponse({'status': 'warning', 'message': 'Update queued, but no administrators found to notify.'}, status=200)

                try:
                    subject = f"[SKAAL-CEN-{queue_item.id}] New Census Edit Pending Approval"
                    context = {'vet_name': user.get_full_name(), 'census_id': census.pk, 'user_note': queue_item.request_note}
                    html_content = render_to_string('emails/census_edit_status.html', context)
                    email = EmailMultiAlternatives(subject, "Pending census edit.", settings.DEFAULT_FROM_EMAIL, admin_emails)
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                except Exception:
                    return JsonResponse({'status': 'warning', 'message': 'Update submitted, but the email notification failed to send.'}, status=200)

                return JsonResponse({'status': 'success', 'message': 'Your updates have been submitted to the administrator for verification.'})

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'System error: {str(e)}'}, status=500)
        
        else:
            errors = {**form.errors, **{f'formset-{i}': e for i, f in enumerate(formset.forms) for e in f.errors}}
           
            return JsonResponse({'status': 'error', 'message': 'Please correct the highlighted errors.', 'errors': errors}, status=400)

    else:
        form = CensusForm(instance=census, user=user)
        formset = FormSetClass(instance=census, user=user, prefix='records')

    return render(request, 'vet/census_form.html', {
        'form': form,
        'formset': formset,
        'is_edit': True,
        'census': census,
        'existing_records': existing_records
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
    # parts = location.split()
    # if len(parts) == 6 and parts[0] == "Line":
    #     initial_line = f"{parts[0]} {parts[1]}"
    #     initial_block = f"{parts[2]} {parts[3]}"
    #     initial_pen = f"{parts[4]} {parts[5]}"
    parts = location.split()
    if len(parts) >= 4 and parts[0] == "Line":
        initial_line = f"{parts[0]} {parts[1]}"
        initial_block = f"{parts[2]} {parts[3]}"
        initial_pen = " ".join(parts[4:]) if len(parts) > 4 else ""
    elif len(parts) >= 2 and parts[0].lower() == "denmark":
        initial_line = "Denmark"
        # Handles "Denmark Block A" or "Denmark 1 Block A" variants
        if parts[1].lower() == "block" or len(parts) == 3:
            initial_block = f"{parts[1]} {parts[2]}" if len(parts) >= 3 else ""
            initial_pen = " ".join(parts[3:]) if len(parts) > 3 else ""
        else:
            initial_line = f"{parts[0]} {parts[1]}"
            initial_block = f"{parts[2]} {parts[3]}" if len(parts) >= 4 else ""
            initial_pen = " ".join(parts[4:]) if len(parts) > 4 else ""

    # Paddock example: "Paddock 4" or "Paddock A"
    if location.startswith("Paddock"):
        initial_paddock = location

    # Small ruminant example: "SR Unit 2", "SR Pen 6"
    if location.lower().startswith("sr"):
        initial_small_ruminant = location
        

    

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

                    elif isinstance(value, (datetime.date, datetime.datetime)):
                        # ✅ Convert date/datetime objects to ISO string for JSON storage
                        pending_data[key] = value.isoformat()
                      
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
        'event_model': EventType,
      

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