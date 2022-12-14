from django import forms
from .models import *
from django.forms import modelformset_factory


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ('truck', 'cat_name1', 'item', 'checkout')

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('motor_name', 'motor_desc', 'motor_image1', 'motor_image2')


DieselFormSet = modelformset_factory(
    Diesel, fields=('motor', 'desc', 'location',  'cat_name3',  'liters', 'price'), extra=1
)

MaintenanceFormSet = modelformset_factory(
    Maintenance, fields=('items', 'price'), extra=1
)
