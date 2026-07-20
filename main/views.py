from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render,  get_object_or_404
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string
from datetime import timedelta,datetime
# from django.db.models import F
from django.db.models.functions import Lower, TruncMonth
from django.utils.timezone import localtime, now, localdate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from drugapp.models import Dispatch, Drug, InventoryLog, PendingStockUpdate
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from drugapp.forms import DrugForm, DispatchForm, UnitForm, AdminDispatchForm, DispatchEditForm, DispatchFilter, UpdateDrugQuantityForm, DrugFilterForm
from itertools import chain
from django.utils import timezone
from django.db.models import Q, F, Count, Sum, Max, Case, When, IntegerField
from drugapp.forms import DrugForm, DispatchForm, UnitForm, DispatchEditForm, DispatchFilter, UpdateDrugQuantityForm, DrugFilterForm
from farmrecord.models import EventType, Census, CensusRecord, PendingEventEdit, Animals, AnimalType, CensusApprovalQueue, PiggeryLine, PiggeryCensusRecord, CensusProjection
import calendar
from django.core.exceptions import FieldDoesNotExist
from .forms import AdminEventEditReviewForm
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.conf import settings
from collections import defaultdict
from django.db import transaction
from veterinary.forms import *
from .services import run_projection_calculation
from .services import run_projection_calculation

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Invalid credentials. Please check your details and try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'profile'):
            if user.profile.is_boss:
              return reverse_lazy('main:main_index')
            elif user.profile.is_supervisor:
              return reverse_lazy('farmrecord:supervisor_index')
            elif user.profile.is_drug:
              return reverse_lazy('drugapp:drug_index')
            elif (
                user.profile.is_vet
                or user.profile.is_vet_piggery
                or user.profile.is_vet_paddock
                or user.profile.is_vet_smallruminant
            ):
                return reverse_lazy('veterinary:vet_index')
            # elif user.profile.is_vet:
            #   return reverse_lazy('veterinary:vet_index')
        return reverse_lazy('main:main_index')




class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login') 


@login_required
def drugs_inventory_land(request):
  drugs_records = Drug.objects.all().order_by('-entered_at')
  dispatch_records = Dispatch.objects.all().order_by('-dispatched_at')

  return render(request, 'main/drug-inventory-page.html', {'drugs_records':drugs_records, 'dispatch_records':dispatch_records})


@login_required
def main_index(request):
    low_stock_drugs = Drug.objects.filter(
        restock_quantity_notify__gt=0,
        quantity__lte=F('restock_quantity_notify')
    )
    today = localdate()
    yesterday = today - timedelta(days=1)

    today_dispatches = Dispatch.objects.filter(dispatched_at__date=today)
    pending_updates = PendingStockUpdate.objects.filter(approved=False)
    # --- FIXED: Translate status choices into actual model flags ---
    current_status = request.GET.get('status', 'pending')
    
    if current_status == 'approved':
        # Processed and approved is True
        census_edits = CensusApprovalQueue.objects.filter(is_processed=True, approved=True)
    elif current_status == 'rejected':
        # Processed and approved is False
        census_edits = CensusApprovalQueue.objects.filter(is_processed=True, approved=False)
    else:
        # Default: 'pending' (not yet processed)
        current_status = 'pending'
        census_edits = CensusApprovalQueue.objects.filter(is_processed=False)

    # Order by submission timestamp
    census_edits = census_edits.order_by('-created_at')
    # ---------------------------------------------------------------
    # --------------------------------------------
    pending_event_edits = PendingEventEdit.objects.filter(status='pending')

    pending_updates_count = pending_updates.count() if request.user.is_staff or request.user.is_superuser else 0

    now_time = now()
    last_24_hours = now_time - timedelta(hours=24)

    new_drugs = Drug.objects.filter(entered_at__gte=last_24_hours)
    restocked_logs = InventoryLog.objects.filter(
        updated_at__gte=last_24_hours,
        new_quantity__gt=F('previous_quantity')
    ).select_related('drug')
    restocked_drugs = Drug.objects.filter(id__in=restocked_logs.values_list('drug_id', flat=True))
    combined_new_drugs = list(set(chain(new_drugs, restocked_drugs)))

    # yesterday_events = EventType.objects.filter(created_at__date=yesterday)

    # Get latest timestamp
    latest_event_date = EventType.objects.aggregate(
        latest_date=Max('created_at__date')
    )['latest_date']

    # Get all events from that date
    if latest_event_date:
        events_by_date = EventType.objects.filter(created_at__date=latest_event_date)
    else:
        events_by_date = EventType.objects.none()

    # Split by animal type (adjust names based on your DB values)
    piggery_events = events_by_date.filter(
    animal_type__animal__animal_name__iexact="pig"
    )

    paddock_events = events_by_date.filter(
        animal_type__animal__animal_name__iexact="cattle"
    )

    small_ruminant_events = events_by_date.filter(
        animal_type__animal__animal_name__in=["sheep", "goat"]
    )

    # Resolve updated animal type IDs into objects
    for p in pending_event_edits:
        animal_type_id = p.data.get("animal_type")

        if animal_type_id:
            try:
                p.animal_type_obj = AnimalType.objects.get(id=animal_type_id)
            except AnimalType.DoesNotExist:
                p.animal_type_obj = None
        else:
            p.animal_type_obj = None

    # Get latest census per animal
    # Get latest census per animal (FIXED LOGIC)

    piggery_total = 0
    paddock_total = 0
    # sheep_total = 0
    # goat_total = 
    # sheep_breakdown = defaultdict(int)
    # goat_breakdown = defaultdict(int)

    # PIG
    # Use annotation to calculate sum excluding geese and crocs
    latest_pig = Census.objects.filter(
        animal__animal_name__iexact="pig"
    ).annotate(
        sum_adults=Sum(
            Case(
                When(piggery_records__line__name__icontains='goose', then=0),
                When(piggery_records__line__name__icontains='crocodile', then=0),
                default=F('piggery_records__number'),
                output_field=IntegerField()
            )
        ),
        sum_piglets=Sum('piggery_records__total_piglets')
    ).order_by('-census_date').first()

    piggery_total = 0
    if latest_pig:
        piggery_total = (latest_pig.sum_adults or 0) + (latest_pig.sum_piglets or 0)

    # CATTLE
    latest_cattle = Census.objects.filter(
        animal__animal_name__iexact="cattle"
    ).order_by('-census_date').first()

    if latest_cattle:
        paddock_total = latest_cattle.records.aggregate(
            total=Sum('number_of_animals')
        )['total'] or 0


   

    # Get latest SMALL RUMINANT census (stored as "sheep")
    latest_small_ruminant = Census.objects.filter(
        animal__animal_name__iexact="sheep"
    ).order_by('-census_date').first()


    sheep_total = 0
    goat_total = 0

    if latest_small_ruminant:
        for record in latest_small_ruminant.records.select_related('animal_type'):
            name = record.animal_type.animal_type_name.lower()
            count = record.number_of_animals

            # SHEEP TYPES
            if name in ['ram', 'ewe', 'lamb', 'weaner (sheep)']:
                sheep_total += count

            # GOAT TYPES
            elif name in ['buck', 'doe', 'kid', 'weaner (goat)']:
                goat_total += count

    # Add this logic to process/hydrate the records for the template
    processed_census_edits = []
    for queue_item in census_edits:
        payload = queue_item.form_data_payload or {}
        records_payload = payload.get('records', [])
        
        # Check if this census has piggery records to determine logic
        is_piggery = queue_item.census.piggery_records.exists()
        
        # Build baseline map for comparison
        if is_piggery:
            db_records = {r.line_id: {'n': r.number, 'p': r.total_piglets, 'note': r.note} for r in queue_item.census.piggery_records.all()}
        else:
            db_records = {r.animal_type_id: {'n': r.number_of_animals, 'note': ''} for r in queue_item.census.records.all()}

        processed_records = []
        for item in records_payload:
            # Handle different keys for Piggery vs Standard
            type_id = item.get('line') if is_piggery else item.get('animal_type')
            count = item.get('number') if is_piggery else item.get('number_of_animals')
            note = item.get('note', '')  # Get the note from payload

            # Extract new values
            new_n = item.get('number') if is_piggery else item.get('number_of_animals')
            new_p = item.get('piglets', 0) if is_piggery else 0
            new_note = item.get('note', '')
            # Build baseline map for comparison

            # Fetch old data
            old_data = db_records.get(type_id, {})
        
            
            # Fetch human-readable name
            try:
                if is_piggery:
                    # FIX: Using the correct model name PiggeryLine
                    type_obj = PiggeryLine.objects.get(id=type_id) 
                    type_name = f"{type_obj.name} ({type_obj.specification})"
                else:
                    type_obj = AnimalType.objects.get(id=type_id)
                    type_name = type_obj.animal_type_name
            except (PiggeryLine.DoesNotExist, AnimalType.DoesNotExist):
                type_name = "Unknown"

            processed_records.append({
                'animal_type_name': type_name,
                'new_count': new_n,
                'old_count': old_data.get('n', 0),
                'new_piglets': new_p,
                'old_piglets': old_data.get('p', 0),
                'new_note': new_note,
                'old_note': old_data.get('note', ''),
                'is_deleted': item.get('DELETE', False),
                # Flags for highlighting
                'count_changed': old_data.get('n') != new_n,
                'piglets_changed': is_piggery and (old_data.get('p') != new_p),
                'note_changed': old_data.get('note') != new_note,
                'is_piggery': is_piggery
            })

        queue_item.records = processed_records
        processed_census_edits.append(queue_item)
    context = {
        'low_stock_drugs': low_stock_drugs,
        'today_dispatches': today_dispatches,
        'today_date': today,
        'pending_updates': pending_updates,
        'census_edits': processed_census_edits,
        # 'census_edits': census_edits,               # ADDED
        'current_status': current_status,           # ADDED
        'pending_event_edits': pending_event_edits,
        'pending_updates_count': pending_updates_count,
        'recent_drugs': combined_new_drugs,
        # 'yesterday_events': yesterday_events,
        'show_prompt': True,
        'latest_event_date': latest_event_date,
        'piggery_events': piggery_events,
        'paddock_events': paddock_events,
        'small_ruminant_events': small_ruminant_events,
        'piggery_total': piggery_total,
        'paddock_total': paddock_total,
        'sheep_total': sheep_total,
        'goat_total': goat_total,
        # 'sheep_breakdown': dict(sheep_breakdown),
        # 'goat_breakdown': dict(goat_breakdown),
    }

    return render(request, 'main/index.html', context)

# @login_required
# def approve_census_edit(request, edit_id):
#     # Only allow staff or superusers to process approvals
#     if not (request.user.is_staff or request.user.is_superuser):
#         messages.error(request, "You do not have permission to approve census changes.")
#         return redirect('main:main_index')

#     if request.method == "POST":
#         queue_item = get_object_or_404(CensusApprovalQueue, id=edit_id, is_processed=False)
#         action = request.POST.get('action')
#         admin_note = request.POST.get('admin_note', '').strip()

#         with transaction.atomic():
#             if action == 'approve':
#                 payload = queue_item.form_data_payload or {}
                
#                 # 1. Update the parent Census metadata if note or date changed
#                 census = queue_item.census
#                 if 'notes' in payload:
#                     census.notes = payload['notes']
#                 if 'census_date' in payload:
#                     census.census_date = payload['census_date']
#                 census.is_pending_review = False
#                 census.save()

#                 # 2. Extract and process the formset records from the JSON payload
#                 # Adjust 'records' to match the exact key name you use to save your formset list
#                 records_data = payload.get('records', [])
                
#                 for record in records_data:
#                     # Case A: Record marked for deletion
#                     if record.get('is_deleted'):
#                         CensusRecord.objects.filter(
#                             census=census, 
#                             animal_type_id=record.get('animal_type_id')
#                         ).delete()
                    
#                     # Case B: Update existing or create new record row
#                     else:
#                         animal_type_id = record.get('animal_type_id')
#                         new_count = record.get('new_count', 0)
                        
#                         if animal_type_id:
#                             CensusRecord.objects.update_or_create(
#                                 census=census,
#                                 animal_type_id=animal_type_id,
#                                 defaults={'number_of_animals': new_count}
#                             )

#                 # Force recalculate totals via your model's built-in helper method
#                 census.update_total()
                
#                 queue_item.approved = True
#                 messages.success(request, f"Census changes for {census.animal.animal_name} successfully approved!")

#             elif action == 'reject':
#                 # Reverting pending flag so it can be edited or resubmitted later
#                 census = queue_item.census
#                 census.is_pending_review = False
#                 census.save()

#                 queue_item.approved = False
#                 messages.warning(request, f"Census update request for {census.animal.animal_name} was rejected.")

#             # Save historical notes if you choose to expand your schema, then mark processed
#             queue_item.is_processed = True
#             queue_item.save()

#     return redirect('main:main_index')


# @login_required
# def approve_census_edit(request, edit_id):
#     # Only allow staff or superusers to process approvals
#     if not (request.user.is_staff or request.user.is_superuser):
#         messages.error(request, "You do not have permission to approve census changes.")
#         return redirect('main:main_index')

#     if request.method == "POST":
#         queue_item = get_object_or_404(CensusApprovalQueue, id=edit_id, is_processed=False)
#         action = request.POST.get('action')
#         admin_comment = request.POST.get('admin_comment', '').strip()

#         # Capture the vet (the user who requested the change) before saving
#         vet = queue_item.requested_by

#         with transaction.atomic():
#             if action == 'approve':
#                 payload = queue_item.form_data_payload or {}
                
#                 # 1. Update the parent Census metadata if note or date changed
#                 census = queue_item.census
#                 if 'notes' in payload:
#                     census.notes = payload['notes']
#                 if 'census_date' in payload:
#                     census.census_date = payload['census_date']
#                 census.is_pending_review = False
#                 census.save()

#                 # 2. Extract and process the formset records from the JSON payload
#                 # Adjust 'records' to match the exact key name you use to save your formset list
#                 records_data = payload.get('records', [])
                
#                 for record in records_data:

#                     # Use 'animal_type' instead of 'animal_type_id' if that's what is in your JSON
#                     type_id = record.get('animal_type') or record.get('animal_type_id')

#                     # Case A: Record marked for deletion
#                     if record.get('is_deleted'):
#                         CensusRecord.objects.filter(
#                             census=census, 
#                             animal_type_id=type_id
#                         ).delete()
                    
#                     # Case B: Update existing or create new record row
#                     else:
#                         # animal_type_id = record.get('animal_type_id')
#                         # new_count = record.get('new_count', 0)
#                         new_count = record.get('new_count') or record.get('number_of_animals')

                        
                        
#                         if type_id:
#                             CensusRecord.objects.update_or_create(
#                                 census=census,
#                                 animal_type_id=type_id,
#                                 defaults={'number_of_animals': new_count}
#                             )

#                 # Force recalculate totals via your model's built-in helper method
#                 census.update_total()
                
#                 queue_item.approved = True
#                 messages.success(request, f"Census changes for {census.animal.animal_name} successfully approved!")

#             elif action == 'reject':
#                 # Reverting pending flag so it can be edited or resubmitted later
#                 census = queue_item.census
#                 census.is_pending_review = False
#                 census.save()

#                 queue_item.approved = False
#                 messages.warning(request, f"Census update request for {census.animal.animal_name} was rejected.")

#             # --- Email Logic ---
#             # subject = f"Census Update {action.title()}d: {queue_item.census.animal.animal_name}"

#             # Define the past tense mapping
#             status_map = {
#                 'approve': 'Approved',
#                 'reject': 'Rejected'
#             }

#             # Use the map to get the correct string
#             status_text = status_map.get(action, action.title())

#             # Use the mapped variable in your subject
#             subject = f"Census Update {status_text}: {queue_item.census.animal.animal_name}"
            
#             # Prepare context for the email template
#             email_context = {
#                 'vet_name': vet.username,
#                 'animal_name': queue_item.census.animal.animal_name,
#                 'status': status_text,
#                 'admin_comment': admin_comment
#             }
            
#             # Render the HTML content
#             email_body = render_to_string('emails/census_status_update.html', email_context)
            
#             # Send the email
#             email = EmailMessage(
#                 subject=subject,
#                 body=email_body,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[vet.email],
#             )
#             email.content_subtype = "html"  # Crucial for HTML templates
#             email.send(fail_silently=True) # Set to False if you want to catch errors
            
#             # --- End Email Logic ---

#             # Save historical notes if you choose to expand your schema, then mark processed
#             queue_item.is_processed = True
#             queue_item.save()

#     return redirect('main:main_index')


@login_required
def approve_census_edit(request, edit_id):
    # ... (Permission check remains the same)
    # Only allow staff or superusers to process approvals
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "You do not have permission to approve census changes.")
        return redirect('main:main_index')


    if request.method == "POST":
        queue_item = get_object_or_404(CensusApprovalQueue, id=edit_id, is_processed=False)
        action = request.POST.get('action')
        admin_comment = request.POST.get('admin_comment', '').strip()
        vet = queue_item.requested_by

        with transaction.atomic():
            census = queue_item.census
            
            if action == 'approve':
                payload = queue_item.form_data_payload or {}
                
                # 1. Update Metadata
                if 'notes' in payload: census.notes = payload['notes']
                if 'census_date' in payload: census.census_date = payload['census_date']
                census.is_pending_review = False
                census.save()

                # 2. Determine if Piggery
                is_piggery = census.piggery_records.exists()
                records_data = payload.get('records', [])
                
                for record in records_data:
                    # Resolve IDs and values based on type
                    if is_piggery:
                        line_id = record.get('line')
                        new_count = record.get('number', 0)
                        new_piglets = record.get('piglets', 0) 
                        line_note = record.get('note', '') # Ensure this matches your template naming
                    else:
                        type_id = record.get('animal_type') or record.get('animal_type_id')
                        new_count = record.get('new_count') or record.get('number_of_animals')

                    # Case A: Deletion
                    if record.get('is_deleted'):
                        if is_piggery:
                            PiggeryCensusRecord.objects.filter(census=census, line_id=line_id).delete()
                        else:
                            CensusRecord.objects.filter(census=census, animal_type_id=type_id).delete()
                    
                    # Case B: Update/Create
                    else:
                        if is_piggery:
                            PiggeryCensusRecord.objects.update_or_create(
                                census=census,
                                line_id=line_id,
                                defaults={
                                    'number': new_count, 
                                    'total_piglets': new_piglets, # FIX: Include this field
                                    'note': line_note
                                }
                            )
                        else:
                            CensusRecord.objects.update_or_create(
                                census=census,
                                animal_type_id=type_id,
                                defaults={'number_of_animals': new_count}
                            )

                # 3. Recalculate totals
                if is_piggery:
                    # Assuming PiggeryCensusRecord has its own update_total method
                    for pr in census.piggery_records.all():
                        pr.update_total() 
                else:
                    census.update_total()
                
                queue_item.approved = True
                messages.success(request, f"Changes for {census.animal.animal_name} approved!")

            elif action == 'reject':
                census.is_pending_review = False
                census.save()
                queue_item.approved = False
                messages.warning(request, "Update request rejected.")

             # --- Email Logic ---
            # subject = f"Census Update {action.title()}d: {queue_item.census.animal.animal_name}"

            # Define the past tense mapping
            status_map = {
                'approve': 'Approved',
                'reject': 'Rejected'
            }

            # Use the map to get the correct string
            status_text = status_map.get(action, action.title())

            # Use the mapped variable in your subject
            subject = f"Census Update {status_text}: {queue_item.census.animal.animal_name}"
            
            # Prepare context for the email template
            email_context = {
                'vet_name': vet.username,
                'animal_name': queue_item.census.animal.animal_name,
                'status': status_text,
                'admin_comment': admin_comment
            }
            
            # Render the HTML content
            email_body = render_to_string('emails/census_status_update.html', email_context)
            
            # Send the email
            email = EmailMessage(
                subject=subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[vet.email],
            )
            email.content_subtype = "html"  # Crucial for HTML templates
            email.send(fail_silently=True) # Set to False if you want to catch errors
            
            # --- End Email Logic ---

            queue_item.is_processed = True
            queue_item.save()

    return redirect('main:main_index')

@login_required
def approve_event_edit(request, pk):
    pending_edit = get_object_or_404(PendingEventEdit, pk=pk)

    if not request.user.profile.is_boss:
        return HttpResponseForbidden()

    event = pending_edit.event
    form = AdminEventEditReviewForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        action = request.POST.get("action")

        pending_edit.admin_note = form.cleaned_data["admin_note"]
        pending_edit.reviewed_by = request.user
        pending_edit.reviewed_at = timezone.now()

        if action == "approve":
            # Apply changes
            for field, value in pending_edit.data.items():
                try:
                    field_obj = EventType._meta.get_field(field)
                except FieldDoesNotExist:
                    continue

                if field_obj.is_relation:
                    related_model = field_obj.related_model
                    try:
                        value = related_model.objects.get(pk=value)
                    except related_model.DoesNotExist:
                        continue

                setattr(event, field, value)

            event.is_approved = True
            event.save()

            pending_edit.status = "approved"
            messages.success(request, "Event edit approved successfully.")

        elif action == "reject":
            pending_edit.status = "rejected"
            messages.warning(request, "Event edit rejected.")

        pending_edit.save()


    vet_email = pending_edit.submitted_by.email

    if vet_email:
        subject = f"Your Event Edit has been {pending_edit.status.title()}"

        context = {
            'event': event,
            'status': pending_edit.status,  # now correct
            'admin_note': pending_edit.admin_note,
            'vet_note': pending_edit.vet_note,
            'data': pending_edit.data,
            'reviewed_by': request.user,
        }

        html_content = render_to_string('emails/event_edit_status.html', context)
        text_content = f"Your event edit has been {pending_edit.status}"

        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [vet_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

    return redirect('main:main_index')

    return render(request, 'main/review_event_edit.html', {
        'pending_edit': pending_edit,
        'event': event,
        'form': form,
    })


@login_required
def dismiss_event_edit(request, pk):
    pending_edit = get_object_or_404(PendingEventEdit, pk=pk)
    pending_edit.delete()
    messages.info(request, "Event edit dismissed.")
    return redirect('main:main_index')


@login_required
def drugs_inventory_lazy(request):
  sort = request.GET.get('sort', 'entered_at')
  order = request.GET.get('order', 'desc')
  page = int(request.GET.get('page', 1))
  search = request.GET.get('search', '').strip()
  per_page = 10

  next_order = 'desc' if order == 'asc' else 'asc'
  sortable_fields = ['manufacturer_name', 'drug_name', 'batch_number', 'quantity', 'expiry_date', 'entered_at']

  drug_qs = Drug.objects.all()

  if search:
      drug_qs = drug_qs.filter( Q(drug_name__icontains=search) | Q(manufacturer_name__icontains=search))

  if sort in sortable_fields:
      sort_expr = Lower(sort) if sort in ['manufacturer_name', 'drug_name', 'batch_number'] else sort
      drug_qs = drug_qs.order_by(
          sort_expr.desc() if order == 'desc' and hasattr(sort_expr, 'desc') else
          sort_expr if order == 'asc' and hasattr(sort_expr, 'desc') else
          f"-{sort}" if order == 'desc' else f"{sort}"
      )
  else:
      drug_qs = drug_qs.order_by('-entered_at')

  paginator = Paginator(drug_qs, per_page)
  page_obj = paginator.get_page(page)

  data = [
      {
          'id': drug.id,
          'manufacturer_name': drug.manufacturer_name,
          'drug_name': drug.drug_name,
          'batch_number': drug.batch_number,
          'quantity': drug.quantity,
          'expiry_date': drug.expiry_date.strftime('%Y-%m-%d'),
      }
      for drug in page_obj
  ]

  return JsonResponse({
      'results': data,
      'current_page': page_obj.number,
      'total_pages': paginator.num_pages,
      'has_next': page_obj.has_next(),
      'has_previous': page_obj.has_previous(),
      'next_order': next_order,
  })


@login_required 
def drugs_inventory(request):
  return render(request, 'main/record-display.html',)


# @login_required
# def drug_detail(request, drug_id):
#   drug = get_object_or_404(Drug, id=drug_id)
#   return render(request, 'main/drug-info.html', {'drug': drug})

@login_required
def drug_detail(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    
    # Check for pending updates directly in the view
    has_pending = drug.pending_updates.filter(approved=False).exists()
    
    return render(request, 'main/drug-info.html', {
        'drug': drug, 
        'has_pending': has_pending
    })


# @login_required
# def edit_drug(request, drug_id):
#     drug = get_object_or_404(Drug, id=drug_id)

#     if request.method == 'POST':
#         form = DrugForm(request.POST, instance=drug, is_editing=True)
#         if form.is_valid():
#           correct_quantity = form.cleaned_data['quantity']

#           drug.correct_stock(correct_quantity, request.user)

#           messages.success(request, "Drug stock corrected successfully!")
#           return redirect('main:drugs_inventory')
#     else:
#         form = DrugForm(instance=drug)

#     return render(request, 'main/modify-drug.html', {'edit_drug_form': form, 'drug': drug})


# @login_required
# def edit_drug(request, drug_id):
#     drug = get_object_or_404(Drug, id=drug_id)
#     if request.method == 'POST':
#         form = DrugForm(request.POST, instance=drug)
#         if form.is_valid():
#             # Use absolute update for admin corrections
#             drug.update_stock_absolute(form.cleaned_data['quantity'], request.user)
#             messages.success(request, "Stock corrected to new value.")
#             return redirect('main:drugs_inventory')
#     return render(request, 'main/modify-drug.html', {'edit_drug_form': DrugForm(instance=drug)})


@login_required
def edit_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    has_pending = PendingStockUpdate.objects.filter(drug=drug).exists()

    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
        if form.is_valid():
            try:
                drug.update_stock_absolute(form.cleaned_data['quantity'], request.user)
                return JsonResponse({'status': 'success', 'message': 'Stock corrected successfully!'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form submission.'}, status=400)

    return render(request, 'main/modify-drug.html', {
        'edit_drug_form': DrugForm(instance=drug), 
        'drug': drug,
        'has_pending': has_pending
    })


@login_required
def delete_drug(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)

  if request.method == 'POST':
    drug.delete()
    return redirect('main:drugs_inventory')

  return render(request, 'main/confirm_delete.html', {'drug': drug})


@login_required
def drug_filter(request):
  if request.method == 'GET':
      drug_query = DrugFilterForm(request.GET)
      if drug_query.is_valid():
          start_date = drug_query.cleaned_data.get('start_date')
          end_date = drug_query.cleaned_data.get('end_date')
          drug_name = drug_query.cleaned_data.get('drug_name')
          filters = {}

          # Apply filters
          if start_date:
              filters['entered_at__gte'] = start_date
          if end_date:
              filters['entered_at__lte'] = datetime.combine(end_date, datetime.max.time())
          if drug_name:
              filters['drug_name__icontains'] = drug_name

          # Query the filtered dispatches
          result = Drug.objects.filter(**filters).order_by('-entered_at')
        

          return render(request, 'main/filter-drug-list.html', {'drugs': result, 'drug_query': drug_query})

  else:
    drug_query = DrugFilterForm()

  return render(request, 'main/filter-drug-list.html', {'drug_query': drug_query})

# @login_required
# def update_drug_quantity(request, drug_id):
#     drug = get_object_or_404(Drug, id=drug_id)
    
#     if request.method == "POST":
#         form = UpdateDrugQuantityForm(request.POST)
#         if form.is_valid():
#             added_amount = form.cleaned_data["quantity"]
            
#             try:
#                 # 1. Admin/Staff: Perform additive update immediately
#                 if request.user.is_staff or request.user.is_superuser:
#                     drug.update_stock_additive(added_amount, request.user)
#                     messages.success(request, "Stock updated successfully!")
                
              
#                 else:
#                     PendingStockUpdate.objects.create(
#                         drug=drug,
#                         requested_quantity=added_amount,
#                         requested_by=request.user
#                     )
#                     messages.info(request, "Stock update request submitted for approval.")
                    
#             except Exception as e:
#                 # Catch potential errors (like negative math)
#                 messages.error(request, f"Update failed: {str(e)}")
#         else:
#             messages.error(request, "Invalid form data.")

#     else:
#         form = UpdateDrugQuantityForm()

#     return render(request, "main/admin-update-drug.html", {"form": form, "drug": drug})


@login_required
def update_drug_quantity(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    
    # Check if a pending request already exists
    has_pending = PendingStockUpdate.objects.filter(drug=drug).exists()

    if request.method == "POST":
        form = UpdateDrugQuantityForm(request.POST)
        if form.is_valid():
            added_amount = form.cleaned_data["quantity"]
            
            try:
                if request.user.is_staff or request.user.is_superuser:
                    if has_pending:
                        return JsonResponse({'status': 'error', 'message': 'Cannot update: A pending request exists.'}, status=400)
                    
                    drug.update_stock_additive(added_amount, request.user)
                    return JsonResponse({'status': 'success', 'message': 'Stock updated successfully!'})
                
                else:
                    if has_pending:
                        return JsonResponse({'status': 'error', 'message': 'You already have a pending request for this drug.'}, status=400)
                    
                    PendingStockUpdate.objects.create(
                        drug=drug,
                        requested_quantity=added_amount,
                        requested_by=request.user
                    )
                    return JsonResponse({'status': 'success', 'message': 'Request submitted for approval.'})
                    
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
        return JsonResponse({'status': 'error', 'message': 'Invalid form data.'}, status=400)

    return render(request, "main/admin-update-drug.html", {"form": UpdateDrugQuantityForm(), "drug": drug})

@login_required
def dispatch_drug_main(request):

  return render(request, 'main/dispatch-records.html',)


@login_required
def dispatch_drug_main_lazy(request):
    sort = request.GET.get('sort', 'dispatched_at')
    order = request.GET.get('order', 'desc')
    page = int(request.GET.get('page', 1))
    per_page = 10
    search = request.GET.get('search', '').strip()

    sortable_fields = ['drug__drug_name', 'quantity', 'dispatched_at', 'dispatched_by']
    dispatch_qs = Dispatch.objects.select_related('drug', 'unit', 'dispatched_by')

    if search:
        dispatch_qs = dispatch_qs.filter(drug__drug_name__icontains=search)

    if sort in sortable_fields:
        if sort in ['drug__drug_name', 'dispatched_by']:
            sort_expr = Lower(sort)
        else:
            sort_expr = F(sort)
        dispatch_qs = dispatch_qs.order_by(
            sort_expr.desc() if order == 'desc' else sort_expr.asc()
        )
    else:
        dispatch_qs = dispatch_qs.order_by('-dispatched_at')

    paginator = Paginator(dispatch_qs, per_page)
    page_obj = paginator.get_page(page)

    data = {
        "results": [
            {
                "id": d.id,
                "drug_name": d.drug.drug_name,
                "quantity": d.quantity,
                "unit": d.unit.name,
                "dispatched_by": d.dispatched_by.get_full_name() if d.dispatched_by else "—",
                "dispatched_at": d.dispatched_at.strftime("%Y-%m-%d %H:%M"),
            }
            for d in page_obj
        ],
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
    }

    return JsonResponse(data)


@login_required
def dispatch_filter_main(request):
  if request.method == 'GET':
      dispatch_query = DispatchFilter(request.GET)
      if dispatch_query.is_valid():
          start_date = dispatch_query.cleaned_data.get('start_date')
          end_date = dispatch_query.cleaned_data.get('end_date')
          drug_name = dispatch_query.cleaned_data.get('drug_name')
          filters = {}

          # Apply filters
          if start_date:
            filters['dispatched_at__gte'] = start_date
          if end_date:
            filters['dispatched_at__lte'] = datetime.combine(end_date, datetime.max.time())
          if drug_name:
              filters['drug__drug_name__icontains'] = drug_name

          # Query the filtered dispatches
          result = Dispatch.objects.filter(**filters).order_by('-dispatched_at')

          return render(request, 'main/filter-dispatch-list.html', {'dispatches': result, 'dispatch_filter': dispatch_query})

  else:
    dispatch_query = DispatchFilter()

  return render(request, 'main/filter-dispatch-list.html', {'dispatch_filter': dispatch_query})



@login_required
def edit_dispatch_main(request, dispatch_id):
  dispatch = get_object_or_404(Dispatch, id=dispatch_id)
  
  if request.method == "POST":
    form = DispatchEditForm(request.POST, instance=dispatch)
    if form.is_valid():
      # Save the form, which will trigger the save method on the Dispatch model
      try:
        form.save()  # The model logic handles stock updates
        return redirect('main:dispatch_drug_main')  # Redirect to dispatch list page or wherever
      except ValueError as e:
        messages.error(request, str(e))  # Display error message if not enough stock
  else:
    form = DispatchEditForm(instance=dispatch)

  return render(request, 'main/edit-dispatch.html', {'form': form, 'dispatch': dispatch})


@login_required
def delete_dispatch_main(request, dispatch_id):
  dispatch = get_object_or_404(Dispatch, id=dispatch_id)

  if request.method == "POST":
    dispatch.delete()  # This will also restore the quantity in the `Drug` model
    messages.success(request, "Dispatch record deleted successfully!")
    return JsonResponse({"success": True, "message": "Dispatch record deleted successfully!"})

  return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)


@login_required
def approve_stock_update(request, pending_update_id):
  if not request.user.is_staff and not request.user.is_superuser:
      messages.error(request, "You are not authorized to approve stock updates.")
      return redirect("main:pending_updates_list")

  pending_update = get_object_or_404(PendingStockUpdate, id=pending_update_id)

  drug = pending_update.drug
  previous_quantity = drug.quantity
  drug.quantity += pending_update.requested_quantity
  drug.has_been_edited = False
  drug.save()

  InventoryLog.objects.create(
    drug=drug,
    previous_quantity=previous_quantity,
    new_quantity=drug.quantity,
    updated_by=request.user
  )

  pending_update.approved = True
  pending_update.save()

  messages.success(request, "Stock update approved successfully.")
  return redirect("main:main_index")


@login_required
def dismiss_stock_update(request, pending_update_id):
  if not request.user.is_staff and not request.user.is_superuser:
    messages.error(request, "You are not authorized to dismiss stock updates.")
    return redirect("main:pending_updates_list")

  pending_update = get_object_or_404(PendingStockUpdate, id=pending_update_id)
  pending_update.delete()  # Remove the request from pending updates

  messages.success(request, "Stock update request dismissed successfully.")
  return redirect("main:main_index")


@login_required
def dismiss_low_stock(request):
  if request.method == "POST":
    drug_id = request.POST.get("drug_id")
    Drug.objects.filter(id=drug_id).update(restock_quantity_notify=0)
    return JsonResponse({"success": True})
  return JsonResponse({"success": False})

@login_required
def admin_add_drug(request):
  if request.method == 'POST':
      form = DrugForm(request.POST)
      if form.is_valid():
        drug = form.save(commit=False)
        drug.logged_by = request.user 
        existing_drug = Drug.objects.filter(batch_number=drug.batch_number).first()
        
        if existing_drug:
          # If drug exists, update stock
          previous_quantity = existing_drug.quantity
          existing_drug.update_stock(previous_quantity + drug.quantity, request.user)
          messages.success(request, "Stock updated successfully!")
          return redirect('drugapp:drugs_list')
        else:
          # If new drug, save normally
          drug.save()
          InventoryLog.objects.create(
            drug=drug,
            previous_quantity=0,
            new_quantity=drug.quantity,
            updated_by=request.user
          )
          # messages.success(request, "Drug added successfully!")

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX response
          return JsonResponse({"success": True, "message": "Drug added successfully!"})

        return redirect('main:admin_add_drug')

      else:
       

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Handle AJAX errors
          return JsonResponse({"success": False, "message": "Error adding drug. Please check your input."})

  else:
      form = DrugForm()

  return render(request, 'main/admin-add-drugs.html', {'form': form})


# views.py
@login_required
def admin_dispatch_drug(request):
  if request.method == "POST":
    form = AdminDispatchForm(request.POST)
    if form.is_valid():
      dispatch = form.save(commit=False)
      dispatch.dispatched_by = request.user
      dispatch.save()

      action = request.POST.get("action")
      if action == "continue":
          messages.success(request, "Dispatch saved. You can add another.")
          return redirect("main:admin_dispatch_drug")
      elif action == "proceed":
          messages.success(request, "Dispatch saved. Proceeding...")
          return redirect("main:drugs_inventory")  # or wherever you want
  else:
    form = AdminDispatchForm()

  return render(request, "main/admin-dispatch-drug.html", {"form": form})


@login_required
def small_ruminant_stats(request):
    # ----- Census Data -----
    census_data = (
        Census.objects.filter(animal__animal_name__in=['sheep', 'goat'])
        .annotate(month=TruncMonth('census_date'))
        .values('month')
        .annotate(total=Sum('total_animals'))  # ✅ sum total animals
        .order_by('month')
    )

    census_labels = [calendar.month_name[d['month'].month] for d in census_data]
    census_values = [d['total'] or 0 for d in census_data]

    # ----- Event Data -----
    event_type = request.GET.get('type', 'mortality')
    event_data = (
        EventType.objects.filter(
            animal__animal_name__in=['sheep', 'goat'],
            event_name__iexact=event_type
        )
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('number_of_animals'))  # ✅ sum event animals
        .order_by('month')
    )
  

    event_labels = [calendar.month_name[d['month'].month] for d in event_data]
    event_values = [d['total'] or 0 for d in event_data]

    context = {
        'census_labels': census_labels,
        'census_values': census_values,
        'event_labels': event_labels,
        'event_values': event_values,
        'selected_type': event_type,
    }
    return render(request, 'main/small_ruminant_stats.html', context)

@login_required
def paddock_stats(request):
    census_data = (
        Census.objects.filter(animal__animal_name='cattle')
        .annotate(month=TruncMonth('census_date'))
        .values('month')
        .annotate(total=Sum('total_animals'))
        .order_by('month')
    )

    census_labels = [calendar.month_name[d['month'].month] for d in census_data]
    census_values = [d['total'] or 0 for d in census_data]

    event_type = request.GET.get('type', 'mortality')
    event_data = (
        EventType.objects.filter(
            animal__animal_name='cattle',
            event_name__iexact=event_type
        )
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('number_of_animals'))
        .order_by('month')
    )

    event_labels = [calendar.month_name[d['month'].month] for d in event_data]
    event_values = [d['total'] or 0 for d in event_data]

    context = {
        'census_labels': census_labels,
        'census_values': census_values,
        'event_labels': event_labels,
        'event_values': event_values,
        'selected_type': event_type,
    }
    return render(request, 'main/paddock_stats.html', context)
    
# @login_required
# def piggery_stats(request):

#     # Retrieve individual census records
#     # 1. Order by census_date (oldest to newest)
#     # 2. Slice [:8] to get the 8 most recent (if you want the very latest, use order_by('-census_date')[:8] and then reverse)
    
#     # RECOMMENDED: Get the 8 most recent records
#     census_records = Census.objects.filter(animal__animal_name='pig').order_by('-census_date')[:8]
    
#     # 3. Convert to list and reverse so the chart displays oldest to newest (left to right)
#     census_records = list(reversed(census_records))
#     # Retrieve individual census records to show specific dates
#     census_records = Census.objects.filter(animal__animal_name='pig').order_by('census_date').annotate(
#         sum_adults=Sum(
#             Case(
#                 When(piggery_records__line__name__icontains='goose', then=0),
#                 When(piggery_records__line__name__icontains='crocodile', then=0),
#                 default=F('piggery_records__number'),
#                 output_field=IntegerField()
#             )
#         ),
#         sum_piglets=Sum('piggery_records__total_piglets')
#     )

#     # Use the census date as the label
#     census_labels = [c.census_date.strftime('%d %b %Y') for c in census_records]
#     adult_values = [c.sum_adults or 0 for c in census_records]
#     piglet_values = [c.sum_piglets or 0 for c in census_records]

#     event_type = request.GET.get('type', 'mortality')
#     event_data = (
#         EventType.objects.filter(
#             animal__animal_name='pig',
#             event_name__iexact=event_type
#         )
#         .annotate(month=TruncMonth('created_at'))
#         .values('month')
#         .annotate(total=Sum('number_of_animals'))
#         .order_by('month')
#     )

#     event_labels = [calendar.month_name[d['month'].month] for d in event_data]
#     event_values = [d['total'] or 0 for d in event_data]

#     context = {
#         'census_labels': census_labels,
#         'adult_values': adult_values,
#         'piglet_values': piglet_values,
#         'event_labels': event_labels,
#         'event_values': event_values,
#         'selected_type': event_type,
#     }
#     return render(request, 'main/piggery_stats.html', context)


@login_required
def piggery_stats(request):
    # Set default to 'weekly' if 'census_view' is not provided in GET parameters
    census_view = request.GET.get('census_view', 'weekly')
    
    # Base queryset with annotations
    census_query = Census.objects.filter(animal__animal_name='pig').order_by('census_date').annotate(
        sum_adults=Sum(
            Case(
                When(piggery_records__line__name__icontains='goose', then=0),
                When(piggery_records__line__name__icontains='crocodile', then=0),
                default=F('piggery_records__number'),
                output_field=IntegerField()
            )
        ),
        sum_piglets=Sum('piggery_records__total_piglets')
    )

    if census_view == 'monthly_last':
        # Filter to keep only the latest census record per month
        monthly_census_ids = (
            Census.objects.filter(animal__animal_name='pig')
            .annotate(month=TruncMonth('census_date'))
            .values('month')
            .annotate(latest_id=Max('id'))
            .values_list('latest_id', flat=True)
        )
        census_records = census_query.filter(id__in=monthly_census_ids).order_by('census_date')
    else:
        # Default: Weekly (all progressive records)
        census_records = census_query

    # Use the census date as the label
    census_labels = [c.census_date.strftime('%d %b %Y') for c in census_records]
    adult_values = [c.sum_adults or 0 for c in census_records]
    piglet_values = [c.sum_piglets or 0 for c in census_records]

    event_type = request.GET.get('type', 'mortality')
    event_data = (
        EventType.objects.filter(
            animal__animal_name='pig',
            event_name__iexact=event_type
        )
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('number_of_animals'))
        .order_by('month')
    )

    event_labels = [calendar.month_name[d['month'].month] for d in event_data]
    event_values = [d['total'] or 0 for d in event_data]

    context = {
        'census_labels': census_labels,
        'adult_values': adult_values,
        'piglet_values': piglet_values,
        'event_labels': event_labels,
        'event_values': event_values,
        'selected_type': event_type,
        'selected_census_view': census_view,
    }
    return render(request, 'main/piggery_stats.html', context)

@login_required
def small_ruminant_event_records_admin(request):
    event_type = request.GET.get('event_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    events = EventType.objects.filter(animal__animal_name__in=['sheep', 'goat'])

    if event_type:
        events = events.filter(event_name__iexact=event_type)
    if start_date:
        events = events.filter(created_at__gte=parse_date(start_date))
    if end_date:
        end = parse_date(end_date)
        if end:
            events = events.filter(created_at__lt=end + timedelta(days=1))

    paginator = Paginator(events.order_by('-created_at'), 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle AJAX infinite scroll
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('main/small-ruminant-records-list.html', {'records': page_obj.object_list})
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    context = {
        'page_obj': page_obj,
        'records': page_obj.object_list,
        'event_types': EventType.objects.values_list('event_name', flat=True).distinct(),
        'selected_event': event_type,
    }
    return render(request, 'main/small-ruminant-records-admin.html', context)


    return render(request, 'main/small-ruminant-records-admin.html', context)

@login_required
def small_ruminant_census_records_admin(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # census_records = Census.objects.filter(animal__animal_name__in=['sheep', 'goat'])
    census_records = Census.objects.filter(animal__animal_name__iexact='sheep')

    # ---- Filters ----
    if start_date:
        census_records = census_records.filter(census_date__gte=parse_date(start_date))
    if end_date:
        end = parse_date(end_date)
        if end:
            census_records = census_records.filter(census_date__lt=end + timedelta(days=1))

    # ---- Pagination ----
    paginator = Paginator(census_records.order_by('-census_date'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'census_records': page_obj.object_list,
        'has_next': page_obj.has_next(),
    }

    # ✅ If it's AJAX (from infinite scroll), return only the HTML list part
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'main/includes/_census_records_list.html', context)

    # Otherwise, render the full page
    return render(request, 'main/small_ruminant_census_records_admin.html', context)



@login_required
def paddock_event_records_admin(request):
    event_type = request.GET.get('event_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    events = EventType.objects.filter(animal__animal_name__iexact='cattle')

    if event_type:
        events = events.filter(event_name__iexact=event_type)
    if start_date:
        events = events.filter(created_at__gte=parse_date(start_date))
    if end_date:
        end = parse_date(end_date)
        if end:
            events = events.filter(created_at__lt=end + timedelta(days=1))

    paginator = Paginator(events.order_by('-created_at'), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle AJAX infinite scroll
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('main/paddock-records-list.html', {'records': page_obj.object_list})
        return JsonResponse({'html': html, 'has_next': page_obj.has_next()})

    context = {
        'page_obj': page_obj,
        'records': page_obj.object_list,
        'event_types': EventType.objects.values_list('event_name', flat=True).distinct(),
        'selected_event': event_type,
    }
    return render(request, 'main/paddock-records-admin.html', context)



@login_required
def paddock_census_records_admin(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    census_records = Census.objects.filter(animal__animal_name__iexact='cattle')

    # ---- Filters ----
    if start_date:
        census_records = census_records.filter(census_date__gte=parse_date(start_date))
    if end_date:
        end = parse_date(end_date)
        if end:
            census_records = census_records.filter(census_date__lt=end + timedelta(days=1))

    # ---- Pagination ----
    paginator = Paginator(census_records.order_by('-census_date'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'census_records': page_obj.object_list,
        'has_next': page_obj.has_next(),
    }

    # ✅ AJAX infinite scroll partial
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'main/includes/_census_records_list.html', context)

    return render(request, 'main/paddock_census_records_admin.html', context)



@login_required
def piggery_event_records_admin(request):
    event_type = request.GET.get('event_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    events = EventType.objects.filter(animal__animal_name__iexact='pig')

    if event_type:
        events = events.filter(event_name__iexact=event_type)
    if start_date:
        events = events.filter(created_at__gte=parse_date(start_date))
    if end_date:
        end = parse_date(end_date)
        if end:
            events = events.filter(created_at__lt=end + timedelta(days=1))

    paginator = Paginator(events.order_by('-created_at'), 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # If AJAX, return JSON (for infinite scroll)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('main/piggery-records-list.html', {'records': page_obj.object_list})
        return JsonResponse({
            'html': html,
            'has_next': page_obj.has_next()
        })

    context = {
        'records': page_obj.object_list,
        'page_obj': page_obj,
        'event_types': EventType.objects.values_list('event_name', flat=True).distinct(),
        'selected_event': event_type,
    }
    return render(request, 'main/piggery-records-admin.html', context)


@login_required
def piggery_census_records_admin(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    census_records = Census.objects.filter(animal__animal_name__iexact='pig')

    # ---- Filters ----
    if start_date:
        census_records = census_records.filter(census_date__gte=parse_date(start_date))
    if end_date:
        end = parse_date(end_date)
        if end:
            census_records = census_records.filter(census_date__lt=end + timedelta(days=1))

    
    # Annotate totals
    census_records = Census.objects.filter(animal__animal_name__iexact='pig').annotate(
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
        ),
        grand_total=F('sum_adults') + F('sum_piglets')
    ).prefetch_related('piggery_records__line').order_by('-census_date')

    # ---- Pagination ----
    paginator = Paginator(census_records.order_by('-census_date'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add this:
    lines = PiggeryLine.objects.all()

    # Handle the line update form
    if request.method == 'POST' and 'line_id' in request.POST:
        line_id = request.POST.get('line_id')
        instance = get_object_or_404(PiggeryLine, id=line_id)
        form = PiggeryLineForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Line updated successfully!'})

    context = {
        'page_obj': page_obj,
        'census_records': page_obj.object_list,
        'has_next': page_obj.has_next(),
        'lines': lines,
    }
    

    # ✅ AJAX infinite scroll partial
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'main/includes/_census_records_list.html', context)

    return render(request, 'main/piggery_census_records_admin.html', context)



@login_required
def exotic_animal_records(request):
    # Filter for PiggeryCensusRecords where the line is goose or crocodile
    exotic_records = PiggeryCensusRecord.objects.filter(
        Q(line__name__icontains='goose') | Q(line__name__icontains='crocodile')
    ).select_related('census', 'line').order_by('-census__census_date')

    # Optional: Date filtering if needed
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        exotic_records = exotic_records.filter(census__census_date__gte=parse_date(start_date))
    if end_date:
        exotic_records = exotic_records.filter(census__census_date__lte=parse_date(end_date))

    context = {
        'exotic_records': exotic_records,
    }
    return render(request, 'main/exotic_animal_records.html', context)

@login_required
def admin_event_detail(request, pk):
    event = get_object_or_404(EventType.objects.select_related('animal', 'animal_type'), pk=pk)

    # Determine which list page this event belongs to
    animal_name = event.animal.animal_name.lower()
    if animal_name == "pig":
        back_url = reverse('main:piggery_event_records_admin')
    elif animal_name == "cattle":
        back_url = reverse('main:paddock_event_records_admin')
    elif animal_name in ["sheep", "goat"]:
        back_url = reverse('main:small_ruminant_event_records_admin')
    else:
        back_url = reverse('main:index')  # fallback

    context = {
        'event': event,
        'back_url': back_url
    }
    return render(request, 'main/admin_event_detail.html', context)

@login_required
def admin_delete_event(request, pk):
    event = get_object_or_404(EventType, pk=pk)

    if request.method == 'POST':
        animal_name = event.animal.animal_name.lower()
        event.delete()
        messages.success(request, "Event deleted successfully!")

        # Redirect to the correct list page based on animal type
        if animal_name == "pig":
            return redirect('main:piggery_event_records_admin')
        elif animal_name == "cattle":
            return redirect('main:paddock_event_records_admin')
        elif animal_name in ["sheep", "goat"]:
            return redirect('main:small_ruminant_event_records_admin')
        else:
            return redirect('main:index')  # fallback

    # If GET request, redirect back to event detail
    return redirect('main:admin_event_detail', pk=pk)

@user_passes_test(lambda u: u.is_staff or (hasattr(u, 'profile') and u.profile.is_boss))
def delete_census_admin(request, pk):
    census = get_object_or_404(Census, pk=pk)
    if request.method == 'POST':
        census.delete()
        # Return JSON for your AJAX modal trigger
        return JsonResponse({'status': 'success', 'message': 'Record deleted successfully.'})
    return redirect('main:paddock_census_records_admin')



# @login_required
# def manage_piggery_lines(request):
#     lines = PiggeryLine.objects.all()
#     if request.method == 'POST':
#         line_id = request.POST.get('line_id')
#         instance = get_object_or_404(PiggeryLine, id=line_id)
#         form = PiggeryLineForm(request.POST, instance=instance)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Line updated successfully!")
#             return redirect('main:manage_piggery_lines')
#     return render(request, 'main/manage_lines.html', {'lines': lines})


# @login_required
# def census_dashboard(request, animal_name):
#     animal = get_object_or_404(Animals, animal_name__iexact=animal_name)
    
#     censuses = Census.objects.filter(animal=animal).order_by('-census_date')
    
#     latest_census = censuses[0] if censuses.count() > 0 else None
#     previous_census = censuses[1] if censuses.count() > 1 else None

#     def get_piggery_total(census):
#         if not census:
#             return 0
#         data = PiggeryCensusRecord.objects.filter(census=census)\
#             .exclude(line__name__icontains='croc').exclude(line__name__icontains='goose')\
#             .aggregate(gen=Sum('number'), pig=Sum('total_piglets'))
#         return (data['gen'] or 0) + (data['pig'] or 0)

#     count_latest = get_piggery_total(latest_census) if animal.animal_name.lower() == 'pig' else (latest_census.total_animals if latest_census else 0)
#     count_prev = get_piggery_total(previous_census) if (previous_census and animal.animal_name.lower() == 'pig') else (previous_census.total_animals if previous_census else 0)

#     # DIRECT FETCH: Avoid model accessor bugs by querying CensusProjection directly
#     previous_projection = None
#     if previous_census:
#         previous_projection = CensusProjection.objects.filter(census=previous_census).first()

#     context = {
#         'latest_census': latest_census,
#         'count_latest': count_latest,
#         'previous_census': previous_census,
#         'count_prev': count_prev,
#         'previous_projection': previous_projection,
#         'animal_name': animal.animal_name.capitalize(),
#     }
#     return render(request, 'main/piggery-census-projection.html', context)


@login_required
def census_dashboard(request, animal_name):
    animal = get_object_or_404(Animals, animal_name__iexact=animal_name)
    
    # Get all censuses ordered by date descending
    censuses = Census.objects.filter(animal=animal).order_by('-census_date')
    
    # Prepare a list of dictionaries to hold census + projection data
    census_data = []
    for c in censuses:
        # Calculate count logic
        if animal.animal_name.lower() == 'pig':
            data = PiggeryCensusRecord.objects.filter(census=c)\
                .exclude(line__name__icontains='croc').exclude(line__name__icontains='goose')\
                .aggregate(gen=Sum('number'), pig=Sum('total_piglets'))
            count = (data['gen'] or 0) + (data['pig'] or 0)
        else:
            count = c.total_animals
            
        projection = CensusProjection.objects.filter(census=c).first()
        
        census_data.append({
            'census': c,
            'count': count,
            'projection': projection
        })

    context = {
        'census_data': census_data,
        'animal_name': animal.animal_name.capitalize(),
    }
    return render(request, 'main/piggery-census-projection.html', context)