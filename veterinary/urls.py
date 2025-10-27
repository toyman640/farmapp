from django.urls import path
from veterinary import views

app_name = 'veterinary'

urlpatterns = [
  path('home/', views.vet_index, name='vet_index'),
  path('lazy-dispatched-drugs/', views.dispatch_records_lazy, name='dispatch_records_lazy'),
  path('dispathed-drug(s)-records/', views.dispatch_view, name='dispatch_view'),
  path('lazy-drugs-records/', views.drugs_records_lazy, name='drugs_records_lazy'),
  path('drug(s)-records/', views.drugs_view, name='drugs_view'),
  path("event-reocrd-entry/", views.create_event, name="create_event"),
  path('event-records/', views.event_records, name='event_records'),
  path('event/<int:pk>/', views.event_detail, name='event_detail'),
  path('events/<int:pk>/edit/', views.edit_event, name='edit_event'),
  path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),

]