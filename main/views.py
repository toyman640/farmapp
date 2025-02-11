from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render,  get_object_or_404
from django.urls import reverse_lazy
from django.db.models import F
from django.utils.timezone import localtime, now, localdate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from drugapp.models import Dispatch, Drug, InventoryLog
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

    return render(request, 'main/record-display.html', {'drugs_page_obj':  drugs_page_obj, 'drug_filter':drug_filter})


@login_required
def drug_detail(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)
  return render(request, 'main/drug-info.html', {'drug': drug})


@login_required
def edit_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)

    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
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
              filters['entered_at__lte'] = end_date
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





