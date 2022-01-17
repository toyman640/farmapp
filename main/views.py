from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from farmrecord import views

# Create your views here.

def dashboard(request):
    return render(request, 'main/index.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('main:dashboard')
            else:
                return redirect('farmrecord:index')
        else:
            messages.info(request, 'Username OR Password is incorrect')
           
    return render(request, 'main/login.html')