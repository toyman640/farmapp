from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db.models import F
from django.utils.timezone import localtime, now, localdate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from drugapp.models import Dispatch, Drug


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


