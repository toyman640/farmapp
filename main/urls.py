from unicodedata import name
from django.urls import path
from main import views
from .views import CustomLogoutView

app_name = 'main'


urlpatterns = [
    path('landing/index', views.main_index, name='main_index'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('drug-records/', views.drugs_inventory, name='drugs_inventory'),
    path('drug/<int:drug_id>/details', views.drug_detail, name='drug_detail'),
    path('drug/edit/<int:drug_id>/', views.edit_drug, name='edit_drug'),
    path('drug/<int:drug_id>/delete/', views.delete_drug, name='delete_drug'),
    path('drug-inventory-records/', views.drugs_inventory_land, name="drugs_inventory_land"),
    path('drugs/filter/', views.drug_filter, name='drug_filter'),
    path("update-drug/<int:drug_id>/", views.update_drug_quantity, name="update_drug_quantity"),
    path('dispatch-drug-records/', views.dispatch_drug_main, name='dispatch_drug_main'),
    path('dispatch-drug/', views.admin_dispatch_drug, name='admin_dispatch_drug'),
    path('dispatch-filter-records/', views.dispatch_filter_main, name='dispatch_filter_main'),
    path('dispatch/edit/<int:dispatch_id>/', views.edit_dispatch_main, name='edit_dispatch_main'),
    path("dispatch/delete/<int:dispatch_id>/", views.delete_dispatch_main, name="delete_dispatch_main"),
    # path("pending-updates/", views.pending_stock_updates, name="pending_updates_list"),
    path('dismis-low-stock-admin', views.dismiss_low_stock, name='dismiss_low_stock'),
    path("approve-update/<int:pending_update_id>/", views.approve_stock_update, name="approve_stock_update"),
    path("dismiss-update/<int:pending_update_id>/", views.dismiss_stock_update, name="dismiss_stock_update"),
    path("dispatch-drug-records-lazy/", views.dispatch_drug_main_lazy, name="dispatch_drug_main_lazy"),
    path("drugs-inventory-lazy/", views.drugs_inventory_lazy, name="drugs_inventory_lazy"),
    path("update-inventory", views.admin_add_drug, name="admin_add_drug"),
    path('admin/small-ruminant-records/', views.small_ruminant_records_admin, name='small_ruminant_records_admin'),
]
