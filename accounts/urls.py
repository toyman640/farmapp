from django.urls import path
from accounts import views
from .views import PurchaseAddView

app_name = 'accounts'


urlpatterns = [
    path('', views.account, name='account'),
    path('delete-post/<int:purch_id>', views.delete_purchase, name='delete_purchase'),
    path('purchses', views.purchase_list, name='purchase_list'),
    path('new-record', PurchaseAddView.as_view(), name="purchase_add"),
    path('purchase-records-filter', views.purchase_filter, name='purchase_filter'),
    path('edit-purchase-record/<int:item_id>', views.edit_purchase, name='edit_purchase'),
    
    
]