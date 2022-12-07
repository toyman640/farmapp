from django.urls import path
from logistics import views

app_name = 'logistics'

urlpatterns = [
    path('', views.transport_home, name='transport_home')
]