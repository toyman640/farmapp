from django import forms
from .models import Drug, Dispatch, Unit
from django.core.exceptions import ValidationError
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
  def __init__(self, *args, **kwargs):
    self.is_editing = kwargs.pop('is_editing', False)
    super().__init__(*args, **kwargs)

  class Meta:
    model = Drug
    exclude = ['has_been_edited', 'logged_by']  # Exclude these fields
    widgets = {
        'manufacturing_date': forms.DateInput(attrs={'type': 'date', 'class': 'col-lg-2'}),
        'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'col-lg-2'}),
    }

  def clean(self):
    if self.is_editing:
      return super().clean()
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


# class AdminDispatchForm(DispatchForm):  # ✅ inherits from DispatchForm
#   class Meta(DispatchForm.Meta):
#     widgets = {
#         'drug': forms.Select(attrs={'class': 'select2-drug'}),  # Add searchable dropdown
#     }

# class AdminDispatchForm(DispatchForm):
#   class Meta(DispatchForm.Meta):
#     widgets = {
#         'drug': forms.Select(attrs={'class': 'select2-drug'}),
#     }

#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     # Customize the label to include available quantity
#     self.fields['drug'].queryset = Drug.objects.all()
#     self.fields['drug'].label_from_instance = (
#         lambda obj: f"{obj.drug_name} ({obj.get_pack_and_pieces()})"
#     )

# class AdminDispatchForm(DispatchForm):
#     class Meta(DispatchForm.Meta):
#         widgets = {
#             'drug': forms.Select(attrs={'class': 'select2-drug'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['drug'].queryset = Drug.objects.all()
#         self.fields['drug'].label_from_instance = (
#             lambda obj: f"{obj.drug_name} ({obj.quantity} pieces)"
#         )

class AdminDispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        exclude = ['dispatched_by']  # hide dispatched_by from the form
        widgets = {
            'drug': forms.Select(attrs={'class': 'select2-drug'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # store logged-in user
        self.fields['drug'].queryset = Drug.objects.all()
        self.fields['drug'].label_from_instance = (
            lambda obj: f"{obj.drug_name} ({obj.quantity} pieces)"
        )

    def clean(self):
        cleaned_data = super().clean()
        drug = cleaned_data.get('drug')
        quantity = cleaned_data.get('quantity')

        if drug and quantity:
            if quantity > drug.quantity:
                raise ValidationError({
                    'quantity': f"Not enough stock for {drug.drug_name}. Only {drug.quantity} pieces left."
                })
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.dispatched_by = self.user  # set automatically
        if commit:
            instance.save()
        return instance

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

