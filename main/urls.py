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
    path('goat-mortality-page', views.goat_mota, name='goat_mota'),
    path('goat-cull-page', views.goat_culla, name='goat_culla'),
    path('goat-procurement-page', views.goat_proca, name='goat_proca'),
    path('goat-sale-page', views.goat_salea, name='goat_salea'),
    path('pig-mortality-page', views.pig_mota, name='pig_mota'),
    path('pig-cull-page', views.pig_culla, name='pig_culla'),
    path('pig-sale-page', views.pig_salea, name='pig_salea'),
    path('pig-procurement', views.pig_proca, name='pig_proca'),
    path('sheep-mortality-page', views.sheep_mota, name='sheep_mota'),
    path('sheep-cull-page', views.sheep_culla, name='sheep_culla'),
    path('sheep-sale-page', views.sheep_salea, name='sheep_salea'),
    path('sheep-procurement-page', views.sheep_proca, name='sheep_proca')
]