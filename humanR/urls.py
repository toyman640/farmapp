# from django.urls import path
# from humanR import views

# app_name = 'humanR'

# urlpatterns = [
#     path('HR-section', views.index, name='index'),
#     path('new-worker/', views.new_entry, name='new_entry'),
#     path('workers-list/', views.employ_list, name='employ_list'),
#     path('biodata/<slug>', views.biodata, name='biodata'),
#     path('workers-list/<int:section_id>/', views.worker_list, name='worker_list'),
#     path('search-result', views.worker_check, name='worker_check'),
#     path('salary-calculator', views.calculator, name='calculator'),
#     path('messages-page', views.review_comHR, name='review_comHR'),
#     path('messages-list/<slug>', views.comlist_viewHR, name='comlist_viewHR'),
#     path('delete-employee-rec/<int:emprec_id>', views.delete_emprec, name='delete_emprec'),
#     path('edit-emplyee-record/<int:emp_id>', views.edit_emprec, name='edit_emprec'),
# ]