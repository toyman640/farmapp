# from cProfile import label
# from dataclasses import fields
# from pyexpat import model
# from django import forms
# from django.contrib.auth.models import User
# from farmrecord.models import *
# from humanR.models import *
# from django.core import validators
# from notification.models import Notification
# from django.forms import modelformset_factory



from django import forms
from .models import Animals, AnimalType, EventType, EventImage

class AnimalsForm(forms.ModelForm):
    class Meta:
        model = Animals
        fields = ['animal_name', 'describe_animal']
        widgets = {
            'animal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter animal name'}),
            'describe_animal': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the animal'}),
        }


class AnimalTypeForm(forms.ModelForm):
    class Meta:
        model = AnimalType
        fields = ['animal', 'animal_type_name', 'animal_type_description']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'animal_type_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter animal type name'}),
            'animal_type_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the animal type'}),
        }


class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ['animal', 'animal_type', 'event_name', 'event_description']
        widgets = {
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'animal_type': forms.Select(attrs={'class': 'form-control'}),
            'event_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event name'}),
            'event_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the event'}),
        }


class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ['event', 'image']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False, 'class': 'form-control'}),
        }



# class RemarkForm(forms.ModelForm):
#     title = forms.CharField(label='Title', widget=forms.TextInput(
#         attrs={'class': 'form-control'}))
       
#     # message = forms.CharField(label='Message', widget=forms.TextInput(
#     #     attrs={'class': 'form-control'}))
#     user = forms.ModelChoiceField(label='Send to',queryset=User.objects.all(), widget=forms.Select(
#         attrs={'class': 'form-control'}))    
#     class Meta:
#         model = Notification
#         fields = ('title', 'message', 'user')

# class WorkerForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = ('title_id', 'job_desc', 'section_id', 'employee_SN', 'employee_FN', 'employee_MN', 'address', 'phone', 'sex', 'age', 'bank_num', 'bank_name', 'bvn', 'email', 'id_type', 'id_num', 'signed', 'nok_surname', 'nok_oname', 'nok_address', 'nok_phone', 'nok_relationship', 'guarantor', 'signed', 'verified', 'image_1')
#         exclude = ['date']

# class EmployeeFilter(forms.ModelForm):
#     employee_SN = forms.CharField(required=False, label= 'Surname',  widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Surname'}))
#     employee_FN = forms.CharField(required=False , label='First name' )
#     section_id = forms.ModelChoiceField(label='Section' ,queryset=FarmSection.objects.all(), required=False)
#     title_id = forms.ModelChoiceField(label='Job title', queryset=JobTitle.objects.all(), required=False)
#     class Meta:
#         model = Employee
#         fields = ('section_id', 'title_id', 'employee_SN', 'employee_FN') 


# class EditempRec(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = ('title_id', 'job_desc', 'section_id', 'employee_SN', 'employee_FN', 'employee_MN', 'address', 'phone', 'sex', 'age', 'bank_num', 'bank_name', 'bvn', 'email', 'id_type', 'id_num', 'signed', 'nok_surname', 'nok_oname', 'nok_address', 'nok_phone', 'nok_relationship', 'guarantor', 'signed', 'verified', 'image_1')


