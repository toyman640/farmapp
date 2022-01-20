from unicodedata import name
from django.urls import path
from main import views

app_name = 'main'


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login_page, name='login_page'),
    path('logout-page', views.logout_view, name='logout_view'),
    path('latest-report', views.latest_page, name='latest_page'),
    path('cow-mortality-page', views.cow_mota, name='cow_mota'),
    path('cow-culling-page', views.cow_culla, name='cow_culla'),
    path('cow-sale-page', views.cow_salea, name='cow_salea'),
    path('cow-procurement-page', views.cow_proca, name='cow_proca'),
]