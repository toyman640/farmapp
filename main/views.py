from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render,  get_object_or_404
from django.urls import reverse_lazy
from datetime import timedelta,datetime
from django.db.models import F
from django.db.models.functions import Lower
from django.utils.timezone import localtime, now, localdate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from drugapp.models import Dispatch, Drug, InventoryLog, PendingStockUpdate
from django.contrib import messages
from django.core.paginator import Paginator
from itertools import chain
from django.db.models import Q
from drugapp.forms import DrugForm, DispatchForm, UnitForm, DispatchEditForm, DispatchFilter, UpdateDrugQuantityForm, DrugFilterForm



# class CustomLoginView(LoginView):
#     template_name = 'main/login.html'
#     redirect_authenticated_user = True

#     def form_valid(self, form):
#         # Log the user in
#         response = super().form_valid(form)
#         user = self.request.user

#         # Redirect based on roles
#         if hasattr(user, 'profile'):
#             if user.profile.is_boss:
#                 return redirect('main:main_index')
#             elif user.profile.is_supervisor:
#                 return redirect('farmrecord:dash_index')
#             elif user.profile.is_drug:
#                 return redirect('drugapp:drug_index')
#         return response

# class CustomLoginView(LoginView):
#     template_name = 'main/login.html'
#     redirect_authenticated_user = True

#     def form_valid(self, form):
#         # Log the user in
#         response = super().form_valid(form)
#         return response

#     def get_success_url(self):
#         # Redirect based on roles
#         user = self.request.user
#         if hasattr(user, 'profile'):
#             if user.profile.is_boss:
#                 return reverse_lazy('main:main_index')
#             elif user.profile.is_supervisor:
#                 return reverse_lazy('farmrecord:dash_index')
#             elif user.profile.is_drug:
#                 return reverse_lazy('drugapp:drug_index')
#         # Fallback URL if no role is matched
#         return reverse_lazy('main:main_index')



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
            elif user.profile.is_vet:
              return reverse_lazy('veterinary:vet_index')
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
  low_stock_drugs = Drug.objects.filter(restock_quantity_notify__gt=0, quantity__lte=F('restock_quantity_notify'))
  today = localdate()
  today_dispatches = Dispatch.objects.filter(dispatched_at__date=today)
  pending_updates = PendingStockUpdate.objects.filter(approved=False)
  pending_updates_count = 0
  now_time = now()
  last_24_hours = now_time - timedelta(hours=24)
  if request.user.is_staff or request.user.is_superuser:
    pending_updates_count = pending_updates.count()

  new_drugs = Drug.objects.filter(entered_at__gte=last_24_hours)
  restocked_logs = InventoryLog.objects.filter(
      updated_at__gte=last_24_hours,
      new_quantity__gt=F('previous_quantity')
  ).select_related('drug')

  restocked_drugs = Drug.objects.filter(id__in=restocked_logs.values_list('drug_id', flat=True))
  combined_new_drugs = list(set(chain(new_drugs, restocked_drugs)))
  

  context = {
    'low_stock_drugs': low_stock_drugs,
    'today_dispatches': today_dispatches,
    'today_date': today,
    "pending_updates": pending_updates,
    "pending_updates_count": pending_updates_count,
    "recent_drugs": combined_new_drugs,
  }

  return render(request, 'main/index.html', context)


# @login_required
# def drugs_inventory(request):
#     dispatch_records = Drug.objects.all().order_by('-entered_at')
#     drug_filter = DrugFilterForm()
#     paginator = Paginator(dispatch_records, 10)
#     page_number = request.GET.get('page')
#     drugs_page_obj = paginator.get_page(page_number)
#     pending_updates = PendingStockUpdate.objects.filter(approved=False)

#     return render(request, 'main/record-display.html', {'drugs_page_obj':  drugs_page_obj, 'drug_filter':drug_filter, "pending_updates": pending_updates})

# @login_required 
# def drugs_inventory(request):
#     sort = request.GET.get('sort', 'entered_at')
#     order = request.GET.get('order', 'desc')

#     # Compute next order (toggle)
#     next_order = 'desc' if order == 'asc' else 'asc'

#     # List of allowed sortable fields
#     sortable_fields = ['manufacturer_name', 'drug_name', 'batch_number', 'quantity', 'expiry_date', 'entered_at']

#     # Default queryset
#     dispatch_records = Drug.objects.all()

#     # Apply case-insensitive sorting if valid field
#     if sort in sortable_fields:
#         if sort in ['manufacturer_name', 'drug_name', 'batch_number']:  # String fields
#             sort_expr = Lower(sort)
#         else:  # Non-string fields
#             sort_expr = sort

#         if order == 'desc':
#             dispatch_records = dispatch_records.order_by(sort_expr.desc() if hasattr(sort_expr, 'desc') else f'-{sort}')
#         else:
#             dispatch_records = dispatch_records.order_by(sort_expr if hasattr(sort_expr, 'desc') else f'{sort}')
#     else:
#         dispatch_records = dispatch_records.order_by('-entered_at')

#     # Pagination and context setup
#     drug_filter = DrugFilterForm()
#     paginator = Paginator(dispatch_records, 10)
#     page_number = request.GET.get('page')
#     drugs_page_obj = paginator.get_page(page_number)
#     pending_updates = PendingStockUpdate.objects.filter(approved=False)

#     context = {
#         'drugs_page_obj': drugs_page_obj,
#         'drug_filter': drug_filter,
#         'pending_updates': pending_updates,
#         'current_sort': sort,
#         'current_order': order,
#         'next_order': next_order,
#     }
#     return render(request, 'main/record-display.html', context)

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
            added_quantity = form.cleaned_data["quantity"]
            new_quantity = drug.quantity + added_quantity  # Add stock

            drug.update_stock(new_quantity, request.user)  # Use model method

            messages.success(request, "Stock updated successfully!")
            return redirect("main:drugs_inventory")
    else:
        form = UpdateDrugQuantityForm()

    return render(request, "main/modify-drug.html", {"update_drug_form": form, "drug": drug})


# @login_required
# def dispatch_drug_main(request):
#   all_dispatch = Dispatch.objects.all().order_by('-dispatched_at')
#   dispatch_filter = DispatchFilter()
#   paginator = Paginator(all_dispatch, 10)
#   page_number = request.GET.get('page')
#   page_obj = paginator.get_page(page_number)


#   return render(request, 'main/dispatch-records.html', {'dispatch_filter': dispatch_filter, 'page_obj': page_obj})


# @login_required
# def dispatch_drug_main(request):
#   sort = request.GET.get('sort', 'dispatched_at')
#   order = request.GET.get('order', 'desc')
#   next_order = 'desc' if order == 'asc' else 'asc'

#   sortable_fields = ['drug__drug_name', 'quantity', 'dispatched_at', 'dispatched_by']
#   dispatch_qs = Dispatch.objects.all()

#   if sort in ['drug__drug_name', 'dispatched_by']:  # string fields
#       sort_expr = Lower(sort)
#   else:
#       sort_expr = sort

#   if sort in sortable_fields:
#       if order == 'desc':
#           dispatch_qs = dispatch_qs.order_by(sort_expr.desc() if hasattr(sort_expr, 'desc') else f'-{sort}')
#       else:
#           dispatch_qs = dispatch_qs.order_by(sort_expr if hasattr(sort_expr, 'desc') else f'{sort}')
#   else:
#       dispatch_qs = dispatch_qs.order_by('-dispatched_at')

#   dispatch_filter = DispatchFilter()
#   paginator = Paginator(dispatch_qs, 10)
#   page_number = request.GET.get('page')
#   page_obj = paginator.get_page(page_number)

#   return render(request, 'main/dispatch-records.html', {
#       'dispatch_filter': dispatch_filter,
#       'page_obj': page_obj,
#       'current_sort': sort,
#       'current_order': order,
#       'next_order': next_order,
#   })

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

  next_order = 'desc' if order == 'asc' else 'asc'
  sortable_fields = ['drug__drug_name', 'quantity', 'dispatched_at', 'dispatched_by']

  dispatch_qs = Dispatch.objects.select_related('drug', 'unit')

  if search:
      dispatch_qs = dispatch_qs.filter(drug__drug_name__icontains=search)

  # Sorting
  if sort in ['drug__drug_name', 'dispatched_by']:
      sort_expr = Lower(sort)
  else:
      sort_expr = sort

  if sort in sortable_fields:
      if order == 'desc':
          dispatch_qs = dispatch_qs.order_by(sort_expr.desc() if hasattr(sort_expr, 'desc') else f'-{sort}')
      else:
          dispatch_qs = dispatch_qs.order_by(sort_expr if hasattr(sort_expr, 'desc') else f'{sort}')
  else:
      dispatch_qs = dispatch_qs.order_by('-dispatched_at')

  # Pagination
  paginator = Paginator(dispatch_qs, per_page)
  page_obj = paginator.get_page(page)

  data = [
      {
          'id': d.id,
          'drug_name': d.drug.drug_name,
          'quantity': d.quantity,
          'unit': d.unit.name,
          'dispatched_at': d.dispatched_at.strftime('%Y-%m-%d'),
          # 'dispatched_by': d.dispatched_by,
          'dispatched_by': str(d.dispatched_by)
      }
      for d in page_obj
  ]

  return JsonResponse({
      'results': data,
      'has_next': page_obj.has_next(),
      'has_previous': page_obj.has_previous(),
      'current_page': page_obj.number,
      'total_pages': paginator.num_pages,
      'next_order': next_order,
  })


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



# @login_required
# def pending_stock_updates(request):
#   if not request.user.is_staff and not request.user.is_superuser:
#     messages.error(request, "You are not authorized to view pending stock updates.")
#     return redirect("main:drugs_list")

#   pending_updates = PendingStockUpdate.objects.filter(approved=False)
#   return render(request, "main/record-display.html", {"pending_updates": pending_updates})



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







