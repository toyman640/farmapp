from django.urls import path
from drugapp import views

app_name = 'drugapp'

urlpatterns = [
  path('drug-app-index', views.drug_index, name='drug_index')
]