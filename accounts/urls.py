from django.urls import path
from accounts import views
from .views import PurchaseAddView,  PurchaseListView

app_name = 'accounts'


urlpatterns = [
    path('', views.account, name='account'),
    # path('purchses', views.purchase_list, name='purchase_list'),
    path('new-record', PurchaseAddView.as_view(), name="purchase_add"),
    path('purchases', PurchaseListView.as_view(), name='purchase_list')
]