from unicodedata import name
from django.urls import path
from farmrecord import views

app_name = 'farmrecord'

urlpatterns = [
    # path("event-reocrd-entry/", views.create_event, name="create_event"),
    # path('test/index', views.dash_index, name='dash_index'),
    path('', views.supervisor_index, name='supervisor_index'),
]

