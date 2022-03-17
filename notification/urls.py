from django.urls import path

from notification import views

# Create your views here.
app_name = 'notification'

urlpatterns = [ 
    path('show/<int:note_id>/', views.show_note, name='show_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note')
]