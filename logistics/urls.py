from django.urls import path
from logistics import views
from .views import DieselAddView

app_name = 'logistics'

urlpatterns = [
    path('', views.transport_home, name='transport_home'),
    path('new-record', DieselAddView.as_view(), name="diesel_add"),
    path('add-new-truck', views.add_truck, name='add_truck'),
    path('fuel-records', views.diesel_post, name='diesel_post'),
    path('add-feed-record', views.feed_rec, name='feed_rec'),
    path('feed-inventory-records', views.feed_post, name='feed_post')
]