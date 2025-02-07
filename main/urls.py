from unicodedata import name
from django.urls import path
from main import views
from .views import CustomLogoutView

app_name = 'main'


urlpatterns = [
    path('landing/index', views.main_index, name='main_index'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('drug-records/', views.drugs_inventory, name='drugs_inventory'),
    path('drug/<int:drug_id>/details', views.drug_detail, name='drug_detail'),
    path('drug/edit/<int:drug_id>/', views.edit_drug, name='edit_drug'),
    path('drug/<int:drug_id>/delete/', views.delete_drug, name='delete_drug'),
    path('drug-inventory-records/', views.drugs_inventory_land, name="drugs_inventory_land"),
    path('drugs/filter/', views.drug_filter, name='drug_filter'),
    path("update-drug/<int:drug_id>/", views.update_drug_quantity, name="update_drug_quantity"),
]