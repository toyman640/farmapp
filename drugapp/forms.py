from django import forms
from .models import Drug, Dispatch, Unit

class UnitForm(forms.ModelForm):
  class Meta:
    model = Unit
    fields = ['name']

class DrugForm(forms.ModelForm):
  class Meta:
    model = Drug
    fields = '__all__'
    widgets = {
      'manufacturing_date': forms.DateInput(attrs={'type': 'date'}),
      'expiry_date': forms.DateInput(attrs={'type': 'date'}),
    }

class DispatchForm(forms.ModelForm):
  class Meta:
    model = Dispatch
    fields = ['drug', 'quantity', 'unit']
