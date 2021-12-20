from django import forms
from django.forms import fields
from farmrecord.models import *
from django.core import validators


class CowmotForm(forms.ModelForm):
    class Meta:
        model = CowMortality
        fields = ('mortality', 'location', 'cow_num', 'bull_num', 'calves', 'section', 'size', 'comment', 'image_1', 'image_2')


