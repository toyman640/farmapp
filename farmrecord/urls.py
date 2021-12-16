from django.urls import path
from farmrecord import views

app_name = 'farmrecord'

urlpatterns = [
    path('', views.test, name='test'),
    path('cow-claving/', views.cow_birth, name='cow_birth'),
    path('cow-culling', views.cow_cull, name='cow_cull'),
    path('cow-mortality', views.cow_motrep, name='cow_motrep'),
    path('cow-procurement', views.cow_proc, name='cow_proc'),
    path('cow-sales', views.cow_sales, name='cow_sales'),
    path('cow-records', views.cow_rec, name='cow_rec'),
    path('goat-birth', views.goat_birth, name='goat_birth'),
    path('goat-culling', views.goat_cull, name='goat_cull'),
    path('goat-mortality', views.goat_motrep, name='goat_motrep'),
    path('goat-procurement', views.goat_proc, name='goat_proc'),
    path('goat-sales', views.goat_sales, name='goat_sales'),
    path('goat-records', views.goat_rec, name='goat_rec'),
    path('pig-birth', views.pig_birth, name='pig_birth'),
    path('pig-culling', views.pig_cull, name='pig_cull'),
    path('pig-mortality', views.pig_motrep, name='pig_motrep'),
    path('pig-procurement', views.pig_proc, name='pig_proc'),
    path('pig-sales', views.pig_sales, name='pig_sales'),
    path('pig-records', views.pig_rec, name='pig_rec'),
    path('sheep-birth', views.sheep_birth, name='sheep_birth'),
    path('sheep-culling', views.sheep_cull, name='sheep_cull'),
    path('sheep-mortality', views.sheep_motrep, name='sheep_motrep'),
    path('sheep-procurement', views.sheep_proc, name='sheep_proc'),
    path('sheep-sales', views.sheep_sales, name='sheep_sales'),
    path('sheep-records', views.sheep_rec, name='sheep_rec'),

]

