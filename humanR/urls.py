from django.urls import path
from humanR import views

app_name = 'humanR'

urlpatterns = [
    path('HR-section', views.index, name='index'),
    path('new-worker/', views.new_entry, name='new_entry')
]