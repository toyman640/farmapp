from django.urls import path

from notification import views

# Create your views here.
app_name = 'notification'

urlpatterns = [ 
    path('show/<slug>/', views.show_note, name='show_note'),
    path('show%hr%/<slug>/', views.show_noteHR, name='show_noteHR'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('delete%hr%/<int:note_id>/', views.delete_notehr, name='delete_notehr')
]