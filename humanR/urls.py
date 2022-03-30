from django.urls import path
from humanR import views

app_name = 'humanR'

urlpatterns = [
    path('HR-section', views.index, name='index'),
    path('new-worker/', views.new_entry, name='new_entry'),
    path('workers-list/', views.employ_list, name='employ_list'),
    path('biodata/<slug>', views.biodata, name='biodata'),
    path('workers-list/<int:section_id>/', views.worker_list, name='worker_list'),
    path('search-result', views.worker_check, name='worker_check')
]