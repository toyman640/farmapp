from unicodedata import name
from django.urls import path
from main import views

app_name = 'main'


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login_page, name='login_page'),
    path('logout-page', views.logout_view, name='logout_view'),
    path('latest-report', views.latest_page, name='latest_page')
]