from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render,  get_object_or_404
from django.urls import reverse_lazy
from django.db.models import F
from django.utils.timezone import localtime, now, localdate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from drugapp.models import Dispatch, Drug
from django.core.paginator import Paginator
from drugapp.forms import DrugForm, DispatchForm, UnitForm, DispatchEditForm, DispatchFilter


class CustomLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        # Log the user in
        response = super().form_valid(form)
        user = self.request.user

        # Redirect based on roles
        if hasattr(user, 'profile'):
            if user.profile.is_boss:
                return redirect('main:main_index')
            elif user.profile.is_supervisor:
                return redirect('farmrecord:dash_index')
            elif user.profile.is_drug:
                return redirect('drugapp:drug_index')
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login') 


@login_required
def main_index(request):
  low_stock_drugs = Drug.objects.filter(restock_quantity_notify__gte=F('quantity'))
  today = localdate()
  today_dispatches = Dispatch.objects.filter(dispatched_at__date=today)

  context = {
    'low_stock_drugs': low_stock_drugs,
    'today_dispatches': today_dispatches, 
  }

  return render(request, 'main/index.html', context)


def drugs_inventory(request):
    dispatch_records = Drug.objects.all()
    paginator = Paginator(dispatch_records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/drug-records.html', {'page_obj': page_obj})


def drug_detail(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)
  return render(request, 'main/drug-info.html', {'drug': drug})


def edit_drug(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)
  if request.method == 'POST':
    form = DrugForm(request.POST, instance=drug)
    if form.is_valid():
      form.save()
      return redirect('main:drugs_inventory')
  else:
    form = DrugForm(instance=drug)
  return render(request, 'main/edit-drug.html', {'form': form, 'drug': drug})


def delete_drug(request, drug_id):
  drug = get_object_or_404(Drug, id=drug_id)

  if request.method == 'POST':
    drug.delete()
    return redirect('main:drugs_inventory')

  return render(request, 'drugapp/confirm_delete.html', {'drug': drug})

