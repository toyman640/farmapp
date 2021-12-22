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
    path('goat-birth', views.goat_birth, name='goat_birth'),
    path('goat-culling', views.goat_cull, name='goat_cull'),
    path('goat-mortality', views.goat_motrep, name='goat_motrep'),
    path('goat-procurement', views.goat_proc, name='goat_proc'),
    path('goat-sales', views.goat_sales, name='goat_sales'),
    path('pig-birth', views.pig_birth, name='pig_birth'),
    path('pig-culling', views.pig_cull, name='pig_cull'),
    path('pig-mortality', views.pig_motrep, name='pig_motrep'),
    path('pig-procurement', views.pig_proc, name='pig_proc'),
    path('pig-sales', views.pig_sales, name='pig_sales'),
    path('sheep-birth', views.sheep_birth, name='sheep_birth'),
    path('sheep-culling', views.sheep_cull, name='sheep_cull'),
    path('sheep-mortality', views.sheep_motrep, name='sheep_motrep'),
    path('sheep-procurement', views.sheep_proc, name='sheep_proc'),
    path('sheep-sales', views.sheep_sales, name='sheep_sales'),
    path('cow-motality-records', views.cow_motrec, name='cow_motrec'),
    path('cow-procurement-records', views.cow_procrec, name='cow_procrec'),
    path('cow-sale-records', views.cow_salerec, name='cow_salerec'),
    path('cow-cull-records', views.cow_cullrec, name='cow_cullrec'),
    path('goat-mortality-records', views.goat_motrec, name='goat_motrec'),
    path('goat-procurement-records', views.goat_procrec, name='goat_procrec'),
    path('goat-cull-records', views.goat_cullrec, name='goat_cullrec'),
    path('goat-sale-records', views.goat_salerec, name='goat_salerec'),
    path('sheep-mortality-records', views.sheep_motrec, name='sheep_motrec'),
    path('sheep-procurement-records', views.sheep_procrec, name='sheep_procrec'),
    path('sheep-cull-records', views.sheep_cullrec, name='sheep_cullrec'),
    path('sheep-sale-records', views.sheep_salerec, name='sheep_salerec'),
    path('pig-sale-records', views.pig_salerec, name='pig_salerec'),
    path('pig-mortality-records', views.pig_motrec, name='pig_motrec'),
    path('pig-procurement-records', views.pig_procrec, name='pig_procrec'),
    path('pig-cull-records', views.pig_cullrec, name='pig_cullrec'),
    path('cow-mortality-record-view/<int:abt_id>', views.cow_motrec_view, name='cow_motrec_view')


]

