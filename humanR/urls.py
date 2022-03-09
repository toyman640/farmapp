from django.urls import path
from humanR import views

app_name = 'humanR'

urlpatterns = [
    path('HR-section', views.index, name='index',)
]