from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render,  get_object_or_404
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from datetime import timedelta,datetime
# from django.db.models import F
from django.db.models.functions import Lower, TruncMonth
from django.utils.timezone import localtime, now, localdate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from drugapp.models import Dispatch, Drug, InventoryLog, PendingStockUpdate
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from drugapp.forms import DrugForm, DispatchForm, UnitForm, AdminDispatchForm, DispatchEditForm, DispatchFilter, UpdateDrugQuantityForm, DrugFilterForm
from itertools import chain
from django.db.models import Q, F, Count, Sum
from drugapp.forms import DrugForm, DispatchForm, UnitForm, DispatchEditForm, DispatchFilter, UpdateDrugQuantityForm, DrugFilterForm
from farmrecord.models import EventType, Census, CensusRecord
import calendar

class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'profile'):
            if user.profile.is_boss:
              return reverse_lazy('main:main_index')
            elif user.profile.is_supervisor:
              return reverse_lazy('farmrecord:dash_index')
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
    pending_updates_count = 0
    now_time = now()
    last_24_hours = now_time - timedelta(hours=24)

    if request.user.is_staff or request.user.is_superuser:
        pending_updates_count = pending_updates.count()

    # New or restocked drugs
    new_drugs = Drug.objects.filter(entered_at__gte=last_24_hours)
    restocked_logs = InventoryLog.objects.filter(
        updated_at__gte=last_24_hours,
        new_quantity__gt=F('previous_quantity')
    ).select_related('drug')
    restocked_drugs = Drug.objects.filter(id__in=restocked_logs.values_list('drug_id', flat=True))
    combined_new_drugs = list(set(chain(new_drugs, restocked_drugs)))

    # 🔹 Get events for only the previous day
    yesterday_events = EventType.objects.filter(created_at__date=yesterday)

    context = {
        'low_stock_drugs': low_stock_drugs,
        'today_dispatches': today_dispatches,
        'today_date': today,
        "pending_updates": pending_updates,
        "pending_updates_count": pending_updates_count,
        "recent_drugs": combined_new_drugs,
        "yesterday_events": yesterday_events,
        'show_prompt': True,
    }

    return render(request, 'main/index.html', context)

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


@login_required
def drug_detail(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)
  return render(request, 'main/drug-info.html', {'drug': drug})


@login_required
def edit_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)

    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug, is_editing=True)
        if form.is_valid():
          correct_quantity = form.cleaned_data['quantity']

          drug.correct_stock(correct_quantity, request.user)

          messages.success(request, "Drug stock corrected successfully!")
          return redirect('main:drugs_inventory')
    else:
        form = DrugForm(instance=drug)

    return render(request, 'main/modify-drug.html', {'edit_drug_form': form, 'drug': drug})


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
          print(result)

          return render(request, 'main/filter-drug-list.html', {'drugs': result, 'drug_query': drug_query})

  else:
    drug_query = DrugFilterForm()

  return render(request, 'main/filter-drug-list.html', {'drug_query': drug_query})


@login_required
def update_drug_quantity(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    if request.method == "POST":
        form = UpdateDrugQuantityForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data["quantity"]
            try:
                drug.request_stock_update(new_quantity, request.user)
                if request.user.is_staff or request.user.is_superuser:
                    messages.success(request, "Stock updated successfully!")
                else:
                    messages.info(request, "Stock update request submitted for approval.")
            except ValueError as e:
                messages.error(request, str(e))
        # ✅ No redirect — stay on the same page
    else:
        form = UpdateDrugQuantityForm()

    return render(request, "main/admin-update-drug.html", {"form": form, "drug": drug})


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
        # print("Form errors:", form.errors)

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


# def small_ruminant_records_admin(request):
#   # Get only events related to sheep and goat
#   records = EventType.objects.filter(animal__animal_name__in=['sheep', 'goat']).order_by('-created_at')
#   context = {'records': records}
#   return render(request, 'main/small-ruminant-records-admin.html', context)


# def small_ruminant_records_admin(request):
#   event_type = request.GET.get('event_type')
#   start_date = request.GET.get('start_date')
#   end_date = request.GET.get('end_date')

#   records = EventType.objects.filter(animal__animal_name__in=['sheep', 'goat'])

#   if event_type:
#       records = records.filter(event_name=event_type)

#   if start_date and end_date:
#       records = records.filter(created_at__range=[start_date, end_date])
#   elif start_date:
#       records = records.filter(created_at__gte=start_date)
#   elif end_date:
#       records = records.filter(created_at__lte=end_date)

#   event_types = EventType.objects.values_list('event_name', flat=True).distinct()

#   context = {
#       'records': records.order_by('-created_at'),
#       'event_types': event_types,
#       'selected_event': event_type,
#   }
#   return render(request, 'main/small-ruminant-records-admin.html', context)


# def small_ruminant_records_admin(request):
#     event_type = request.GET.get('event_type')
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     # ----- Event Records -----
#     records = EventType.objects.filter(animal__animal_name__in=['sheep', 'goat'])

#     if event_type:
#         records = records.filter(event_name=event_type)

#     if start_date and end_date:
#         records = records.filter(created_at__range=[start_date, end_date])
#     elif start_date:
#         records = records.filter(created_at__gte=start_date)
#     elif end_date:
#         records = records.filter(created_at__lte=end_date)

#     event_types = EventType.objects.values_list('event_name', flat=True).distinct()

#     # ----- Census Records -----
#     census_records = (
#         Census.objects.filter(animal__animal_name__in=['sheep', 'goat'])
#         .order_by('-census_date')
#     )

#     # ----- Chart Data (Monthly Totals) -----
#     census_data = (
#         Census.objects.filter(animal__animal_name__in=['sheep', 'goat'])
#         .annotate(month=TruncMonth('census_date'))
#         .values('month')
#         .annotate(total=Count('id'))
#         .order_by('month')
#     )

#     census_months = [d['month'].strftime('%B %Y') for d in census_data]
#     census_totals = [d['total'] for d in census_data]

#     context = {
#         'records': records.order_by('-created_at'),
#         'event_types': event_types,
#         'selected_event': event_type,
#         'census_records': census_records,   # ✅ added this
#         'census_months': census_months,
#         'census_totals': census_totals,
#     }
#     return render(request, 'main/small-ruminant-records-admin.html', context)

# def small_ruminant_stats(request):
#   # ----- Census Data -----
#   census_data = (
#       Census.objects.filter(animal__animal_name__iexact='sheep')
#       .annotate(month=TruncMonth('census_date'))
#       .values('month')
#       .annotate(total=Count('id'))
#       .order_by('month')
#   )

#   census_labels = [calendar.month_name[d['month'].month] for d in census_data]
#   census_values = [d['total'] for d in census_data]

#   # ----- Event Data -----
#   event_type = request.GET.get('type', 'mortality')
#   event_data = (
#       EventType.objects.filter(
#           animal__animal_name__iexact='sheep',
#           event_name__iexact=event_type
#       )
#       .annotate(month=TruncMonth('created_at'))
#       .values('month')
#       .annotate(total=Count('id'))
#       .order_by('month')
#   )


#   event_labels = [calendar.month_name[d['month'].month] for d in event_data]
#   event_values = [d['total'] for d in event_data]

#   context = {
#       'census_labels': census_labels,
#       'census_values': census_values,
#       'event_labels': event_labels,
#       'event_values': event_values,
#       'selected_type': event_type,
#   }
#   return render(request, 'main/small_ruminant_stats.html', context)

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
    print(event_data)

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
    
@login_required
def piggery_stats(request):
    census_data = (
        Census.objects.filter(animal__animal_name='pig')
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
        'census_values': census_values,
        'event_labels': event_labels,
        'event_values': event_values,
        'selected_type': event_type,
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


# @login_required
# def small_ruminant_event_records_admin(request):
#     event_type = request.GET.get('event_type')
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     events = EventType.objects.filter(animal__animal_name__in=['sheep', 'goat'])

#     # ---- Filters ----
#     if event_type:
#         events = events.filter(event_name__iexact=event_type)
#     if start_date:
#         events = events.filter(created_at__gte=parse_date(start_date))
#     if end_date:
#         end = parse_date(end_date)
#         if end:
#             events = events.filter(created_at__lt=end + timedelta(days=1))

#     # ---- Pagination ----
#     paginator = Paginator(events.order_by('-created_at'), 10)  # 10 per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj,
#         'records': page_obj.object_list,
#         'event_types': EventType.objects.values_list('event_name', flat=True).distinct(),
#         'selected_event': event_type,
#     }
#     return render(request, 'main/small-ruminant-records-admin.html', context)

@login_required
def small_ruminant_census_records_admin(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    census_records = Census.objects.filter(animal__animal_name__in=['sheep', 'goat'])

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


# @login_required
# def paddock_event_records_admin(request):
#     event_type = request.GET.get('event_type')
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     events = EventType.objects.filter(animal__animal_name__iexact='cattle')

#     # ---- Filters ----
#     if event_type:
#         events = events.filter(event_name__iexact=event_type)
#     if start_date:
#         events = events.filter(created_at__gte=parse_date(start_date))
#     if end_date:
#         end = parse_date(end_date)
#         if end:
#             events = events.filter(created_at__lt=end + timedelta(days=1))

#     # ---- Pagination ----
#     paginator = Paginator(events.order_by('-created_at'), 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj,
#         'records': page_obj.object_list,
#         'event_types': EventType.objects.values_list('event_name', flat=True).distinct(),
#         'selected_event': event_type,
#     }
#     return render(request, 'main/paddock-records-admin.html', context)


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


# @login_required
# def piggery_event_records_admin(request):
#     event_type = request.GET.get('event_type')
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     events = EventType.objects.filter(animal__animal_name__iexact='pig')

#     # ---- Filters ----
#     if event_type:
#         events = events.filter(event_name__iexact=event_type)
#     if start_date:
#         events = events.filter(created_at__gte=parse_date(start_date))
#     if end_date:
#         end = parse_date(end_date)
#         if end:
#             events = events.filter(created_at__lt=end + timedelta(days=1))

#     # ---- Pagination ----
#     paginator = Paginator(events.order_by('-created_at'), 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'page_obj': page_obj,
#         'records': page_obj.object_list,
#         'event_types': EventType.objects.values_list('event_name', flat=True).distinct(),
#         'selected_event': event_type,
#     }
#     return render(request, 'main/piggery-records-admin.html', context)

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

    return render(request, 'main/piggery_census_records_admin.html', context)
