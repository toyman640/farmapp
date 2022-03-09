from unicodedata import name
from django.urls import path
from main import views

app_name = 'main'


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout-page', views.logout_view, name='logout_view'),
    path('latest-report', views.latest_page, name='latest_page'),
    path('cow-mortality-page', views.cow_mota, name='cow_mota'),
    path('cow-culling-page', views.cow_culla, name='cow_culla'),
    path('cow-sale-page', views.cow_salea, name='cow_salea'),
    path('cow-procurement-page', views.cow_proca, name='cow_proca'),
    path('goat-mortality-page', views.goat_mota, name='goat_mota'),
    path('goat-cull-page', views.goat_culla, name='goat_culla'),
    path('goat-procurement-page', views.goat_proca, name='goat_proca'),
    path('goat-sale-page', views.goat_salea, name='goat_salea'),
    path('pig-mortality-page', views.pig_mota, name='pig_mota'),
    path('pig-cull-page', views.pig_culla, name='pig_culla'),
    path('pig-sale-page', views.pig_salea, name='pig_salea'),
    path('pig-procurement-page', views.pig_proca, name='pig_proca'),
    path('sheep-mortality-page', views.sheep_mota, name='sheep_mota'),
    path('sheep-cull-page', views.sheep_culla, name='sheep_culla'),
    path('sheep-sale-page', views.sheep_salea, name='sheep_salea'),
    path('sheep-procurement-page', views.sheep_proca, name='sheep_proca'),
    path('cattle-records-page', views.cow_all, name='cow_all'),
    path('goat-records-page', views.goat_all, name='goat_all'),
    path('pig-records-page', views.pig_all, name='pig_all'),
    path('sheep-records-page', views.sheep_all, name='sheep_all'),
    path('cow-mortality-filter-results/', views.cowmota_filter, name='cowmota_filter'),
    path('goat-mortality-filter-results/', views.goatmota_filter, name='goatmota_filter'),
    path('pig-mortality-filter-results/', views.pigmota_filter, name='pigmota_filter'),
    path('sheep-mortality-filter-results/', views.sheepmota_filter, name='sheepmota_filter'),
    path('cow-sale-filter-results/', views.cowsalea_filter, name='cowsalea_filter'),
    path('goat-sale-filter-results/', views.goatsalea_filter, name='goatsalea_filter'),
    path('sheep-sale-filter-results/', views.sheepsalea_filter, name='sheepsalea_filter'),
    path('pig-sale-filter-results/', views.pigsalea_filter, name='pigsalea_filter'),
    path('cow-procurement-filter-results/', views.cowproca_filter, name='cowproca_filter'),
    path('goat-procurement-filter-results/', views.goatproca_filter, name='goatproca_filter'),
    path('pig-procurement-filter-results/', views.pigproca_filter, name='pigproca_filter'),
    path('sheep-procurement-filter-results/', views.sheepproca_filter, name='sheepproca_filter'),
    path('cow-culling-filter-results/', views.cowculla_filter, name='cowculla_filter'),
    path('goat-culling-filter-results/', views.goatculla_filter, name='goatculla_filter'),
    path('sheep-culling-filter-results/', views.sheepculla_filter, name='sheepculla_filter'),
    path('pig-culling-filter-results/', views.pigculla_filter, name='pigculla_filter'),
    path('cow-image-view/<slug>', views.cow_image_view, name='cow_image_view'),
    path('goat-image-view/<slug>', views.goat_image_view, name='goat_image_view'),
    path('sheep-image-view/<slug>', views.sheep_image_view, name='sheep_image_view'),
    path('pig-image-view/<slug>', views.pig_image_view, name='pig_image_view'),
    path('write-comment/remark', views.review_page, name='review_page')
]