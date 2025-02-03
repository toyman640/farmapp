# from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.db.models.aggregates import Count, Sum
# from django.db.models.functions import TruncMonth, TruncDay
# from farmrecord.models import *
# from django.core.paginator import Paginator
# from farmrecord.forms import *
# from datetime import timedelta
# from django.contrib.auth.decorators import user_passes_test
# from django.db.models import F
# from humanR.models import FarmSection, Employee
# from datetime import datetime

# today = datetime.today()

# year = today.year
# month = today.month
# day = today.day


# # Create your views here.

# def staff_required(login_url=None):
#     return user_passes_test(lambda u: u.is_staff, login_url=login_url)


from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


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
    return render(request, 'main/index.html')


