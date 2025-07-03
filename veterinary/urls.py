from django.urls import path
from veterinary import views

app_name = 'veterinary'

urlpatterns = [
  path('home/', views.vet_index, name='vet_index'),
]