from unicodedata import name
from django.urls import path
from main import views
from .views import CustomLogoutView

app_name = 'main'


urlpatterns = [
    path('test/index', views.main_index, name='main_index'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]