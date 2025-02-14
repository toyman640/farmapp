from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render,  get_object_or_404
from django.urls import reverse_lazy
from datetime import timedelta,datetime
from django.db.models import F
from django.utils.timezone import localtime, now, localdate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from drugapp.models import Dispatch, Drug, InventoryLog, PendingStockUpdate
from django.contrib import messages
from django.core.paginator import Paginator
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
  low_stock_drugs = Drug.objects.filter(restock_quantity_notify__gte=F('quantity'))
  today = localdate()
  today_dispatches = Dispatch.objects.filter(dispatched_at__date=today)

  context = {
    'low_stock_drugs': low_stock_drugs,
    'today_dispatches': today_dispatches,
    'today_date': today,
  }

  return render(request, 'main/index.html', context)


@login_required
def drugs_inventory(request):
    dispatch_records = Drug.objects.all().order_by('-entered_at')
    drug_filter = DrugFilterForm()
    paginator = Paginator(dispatch_records, 10)
    page_number = request.GET.get('page')
    drugs_page_obj = paginator.get_page(page_number)
    pending_updates = PendingStockUpdate.objects.filter(approved=False)

    return render(request, 'main/record-display.html', {'drugs_page_obj':  drugs_page_obj, 'drug_filter':drug_filter, "pending_updates": pending_updates})


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


@login_required
def dispatch_drug_main(request):
  all_dispatch = Dispatch.objects.all().order_by('-dispatched_at')
  dispatch_filter = DispatchFilter()
  paginator = Paginator(all_dispatch, 10)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)


  return render(request, 'main/dispatch-records.html', {'dispatch_filter': dispatch_filter, 'page_obj': page_obj})


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
  return redirect("main:drugs_inventory")







