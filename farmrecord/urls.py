from unicodedata import name
from django.urls import path
from farmrecord import views

app_name = 'farmrecord'

urlpatterns = [
    # path("event-reocrd-entry/", views.create_event, name="create_event"),
    # path('test/index', views.dash_index, name='dash_index'),
    path('', views.supervisor_index, name='supervisor_index'),
    # path('census-records/', views.census_records, name='census_records'),
    path('census-records/exotic/', views.create_exotic_animal_census, name='create_exotic_animal_census'),
    path('exotic-animal-census-records/',views.exotic_animal_census_records,name='exotic_animal_census_records'
),
]

