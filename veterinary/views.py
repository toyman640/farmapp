from django.shortcuts import render, redirect
from .forms import EventForm
from drugapp.models import Dispatch, Drug, InventoryLog
from django.utils.timezone import localtime, now, localdate, timedelta
from django.db.models import Q
from itertools import chain
from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from farmrecord.models import EventType
from django.urls import reverse

# Create your views here.

@login_required
def vet_index(request):
  today = localdate()
  now_time = now()
  last_24_hours = now_time - timedelta(hours=24)
  today_dispatches = Dispatch.objects.filter(dispatched_at__date=today)
  new_drugs = Drug.objects.filter(entered_at__gte=last_24_hours)
  restocked_logs = InventoryLog.objects.filter(updated_at__gte=last_24_hours,new_quantity__gt=F('previous_quantity')).select_related('drug')
  restocked_drugs = Drug.objects.filter(id__in=restocked_logs.values_list('drug_id', flat=True))
  combined_new_drugs = list(set(chain(new_drugs, restocked_drugs)))

  context = {
    'today_dispatches': Dispatch.objects.filter(dispatched_at__date=today),
    'today_date': today,
    'recent_drugs': combined_new_drugs,
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
#   if request.method == 'POST':
#       form = EventForm(request.POST, request.FILES, user=request.user)
#       if form.is_valid():
#           event = form.save(commit=False)
#           event.save()
#           messages.success(request, "Event created successfully!")
#           return redirect('veterinary:create_event')  # reloads the same page
#       else:
#           messages.error(request, "There was an error submitting the form. Please check your input.")
#   else:
#       form = EventForm(user=request.user)

#   return render(request, 'vet/event_form.html', {'form': form})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            event = form.save(commit=False)
            event.save()

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

            messages.success(request, "Event created successfully!")
            return redirect('veterinary:create_event')

        else:
            # Collect detailed field errors
            errors = {
                field: [str(err) for err in errs]
                for field, errs in form.errors.items()
            }

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please correct the highlighted errors.',
                    'errors': errors,
                })

            messages.error(request, "Error saving event. Check your input.")

    else:
        form = EventForm(user=request.user)

    return render(request, 'vet/event_form.html', {'form': form})


# @login_required
# def event_records(request):
#     user = request.user
#     selected_event = request.GET.get('event_type')

#     # Get all event types (for dropdown)
#     all_event_types = EventType.objects.values_list('event_name', flat=True).distinct()

#     # Get all events and filter by vet specialization
#     events = EventType.objects.all().select_related('animal', 'animal_type')

#     if hasattr(user, 'profile'):
#         profile = user.profile
#         if profile.is_vet_piggery:
#             events = events.filter(animal__animal_name='pig')
#         elif profile.is_vet_paddock:
#             events = events.filter(animal__animal_name='cattle')
#         elif profile.is_vet_smallruminant:
#             events = events.filter(animal__animal_name__in=['sheep', 'goat'])
#         elif not profile.is_vet:
#             events = EventType.objects.none()
#     else:
#         events = EventType.objects.none()

#     # Apply event type filter if selected
#     if selected_event:
#         events = events.filter(event_name=selected_event)

#     # Order newest first
#     events = events.order_by('-created_at')

#     context = {
#         'events': events,
#         'event_types': all_event_types,  # ✅ show all event types
#         'selected_event': selected_event,
#     }
#     return render(request, 'vet/entry-records.html', context)


@login_required
def event_records(request):
    user = request.user
    selected_event = request.GET.get('event_type')

    events = EventType.objects.all().select_related('animal', 'animal_type')

    # Default empty event types list
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

    # Filter events by selected type if any
    if selected_event:
        events = events.filter(event_name=selected_event)

    # Order newest first
    events = events.order_by('-created_at')

    context = {
        'events': events,
        'event_types': event_types,
        'selected_event': selected_event,
    }
    return render(request, 'vet/entry-records.html', context)
