from django import forms
from .models import Drug, Dispatch, Unit
from datetime import date

class UnitForm(forms.ModelForm):
  class Meta:
    model = Unit
    fields = ['name']

# class DrugForm(forms.ModelForm):
#   class Meta:
#     model = Drug
#     exclude = ['has_been_edited', 'logged_by'] 
#     widgets = {
#       'manufacturing_date': forms.DateInput(attrs={'type': 'date'}),
#       'expiry_date': forms.DateInput(attrs={'type': 'date'}),
#     }

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        exclude = ['has_been_edited', 'logged_by']  # Exclude these fields
        widgets = {
            'manufacturing_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        restock_quantity_notify = cleaned_data.get('restock_quantity_notify')

        if restock_quantity_notify and quantity and restock_quantity_notify > quantity:
            raise forms.ValidationError(
                {"restock_quantity_notify": "Restock quantity cannot be greater than available stock quantity."}
            )

        return cleaned_data


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

class DispatchFilter(forms.Form):
  start_date = forms.DateField(
      widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'From'}),
      required=False
  )
  end_date = forms.DateField(
      widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'To'}),
      required=False
  )
  drug_name = forms.CharField(
      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Drug Name'}),
      required=False
  )


class UpdateDrugQuantityForm(forms.ModelForm):
  class Meta:
    model = Drug
    fields = ["quantity"]


class DrugFilterForm(forms.Form):
  start_date = forms.DateField(
    widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'From'}),
    required=False
  )
  end_date = forms.DateField(
    widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'To'}),
    required=False
  )
  drug_name = forms.CharField(
    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Drug Name'}),
    required=False
  )

