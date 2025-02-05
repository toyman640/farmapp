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

class DispatchEditForm(forms.ModelForm):
  drug = forms.ModelChoiceField(
    queryset=Drug.objects.all(),
    label="Drug Name",
    widget=forms.Select(attrs={'class': 'form-control'})
  )
  unit = forms.ModelChoiceField(
    queryset=Unit.objects.all(),
    label="Unit",
    widget=forms.Select(attrs={'class': 'form-control'})
  )

  class Meta:
    model = Dispatch
    fields = ['drug', 'quantity', 'unit']
    widgets = {
      'quantity': forms.NumberInput(attrs={'class': 'form-control'})
    }

