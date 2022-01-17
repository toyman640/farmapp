from django.urls import path
from main.views import login_page
from main import views

app_name = 'main'


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login_page, name='login_page')
]