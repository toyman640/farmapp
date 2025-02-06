from django.urls import path
from drugapp import views

app_name = 'drugapp'

urlpatterns = [
  path('drug-app-index', views.drug_index, name='drug_index'),
  path('add-unit/', views.add_unit, name='add_unit'),
  path('units/', views.list_units, name='list_units'),
  path('add-to-inventory/', views.add_drug, name='add_drug'),
  path('drugs-records/', views.drugs_list, name='drugs_list'),
  path('dispatch-drug/', views.dispatch_drug, name='dispatch_drug'),
  path('dismis-low-stock', views.dismiss_low_stock, name='dismiss_low_stock'),
  path('dispatch/edit/<int:dispatch_id>/', views.edit_dispatch, name='edit_dispatch'),
  path("dispatch/delete/<int:dispatch_id>/", views.delete_dispatch, name="delete_dispatch"),
  path('drug/<int:drug_id>/', views.drug_detail, name='drug_detail'),
  path('drug/edit/<int:drug_id>/', views.edit_drug, name='edit_drug'),
  path('drug/<int:drug_id>/delete/', views.delete_drug, name='delete_drug'),
  path('dispatch/filter/', views.dispatch_filter, name='dispatch_filter'),
   path("update-drug/<int:drug_id>/", views.update_drug_quantity, name="update_drug_quantity"),
]