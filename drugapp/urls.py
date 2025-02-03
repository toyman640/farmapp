from django.urls import path
from drugapp import views

app_name = 'drugapp'

urlpatterns = [
  path('drug-app-index', views.drug_index, name='drug_index'),
  path('add-unit/', views.add_unit, name='add_unit'),
  path('units/', views.list_units, name='list_units'),
]