from django import forms
from django.forms import fields
from farmrecord.models import *
from django.core import validators


class CowmotForm(forms.ModelForm):
    class Meta:
        model = CowMortality
        fields = ('mortality', 'location', 'cow_num', 'bull_num', 'calves', 'section', 'size', 'comment', 'image_1', 'image_2')


class GoatmotForm(forms.ModelForm):
    class Meta:
        model = GoatMortality
        fields = ('mortality', 'location', 'doe_num', 'buck_num', 'kid', 'section', 'size', 'comment', 'image_1', 'image_2')

class SheepmotForm(forms.ModelForm):
    class Meta:
        model = SheepMortality
        fields = ('mortality', 'location', 'ram_num', 'ewe_num', 'lamb', 'section', 'size', 'comment', 'image_1', 'image_2')

class PigmotForm(forms.ModelForm):
    class Meta:
        model = PigMortality
        fields = ('mortality', 'location', 'sow_num', 'boar_num', 'pigglet', 'section', 'size', 'comment', 'image_1', 'image_2')

class CowcullForm(forms.ModelForm):
    class Meta:
        model = CowCulling
        fields =('cow_num', 'bull_num', 'section', 'location', 'reason')

class GoatcullForm(forms.ModelForm):
    class Meta:
        model = GoatCulling
        fields =('doe_num', 'buck_num', 'section', 'location', 'reason')

class SheepcullForm(forms.ModelForm):
    class Meta:
        model = SheepCulling
        fields =('ewe_num', 'ram_num', 'section', 'location', 'reason')

class PigcullForm(forms.ModelForm):
    class Meta:
        model = PigCulling
        fields =('sow_num', 'boar_num', 'section', 'location', 'reason')

class CowsaleForm(forms.ModelForm):
    class Meta:
        model = CowSale
        fields =('cow_num', 'size', 'bull_num', 'size1', 'section', 'weight', 'price')

class GoatsaleForm(forms.ModelForm):
    class Meta:
        model = GoatSale
        fields =('doe_num', 'size', 'buck_num', 'size1', 'section', 'weight', 'price')

class SheepsaleForm(forms.ModelForm):
    class Meta:
        model = SheepSale
        fields =('ewe_num', 'size', 'ram_num', 'size1', 'section', 'weight', 'price')

class PigsaleForm(forms.ModelForm):
    class Meta:
        model = PigSale
        fields =('sow_num', 'size', 'boar_num', 'size1', 'section', 'weight', 'price')

class CowprocForm(forms.ModelForm):
    class Meta:
        model = CowProcurement
        fields = ('cow_num', 'size', 'bull_num', 'size1', 'section' )

class GoatprocForm(forms.ModelForm):
    class Meta:
        model = GoatProcurement
        fields = ('buck_num', 'size', 'doe_num', 'size1', 'section' )

class SheepprocForm(forms.ModelForm):
    class Meta:
        model = SheepProcurement
        fields = ('ewe_num', 'size', 'ram_num', 'size1', 'section' )

class PigprocForm(forms.ModelForm):
    class Meta:
        model = PigProcurement
        fields = ('sow_num', 'size', 'boar_num', 'size1', 'section' )

class EditcowMot(forms.ModelForm):
    class Meta:
        model = CowMortality
        fields = ('mortality', 'location', 'cow_num', 'bull_num', 'calves', 'section', 'size', 'comment', 'image_1', 'image_2')

class EditgoatMot(forms.ModelForm):
    class Meta:
        model = GoatMortality
        fields = ('mortality', 'location', 'doe_num', 'buck_num', 'kid', 'section', 'size', 'comment', 'image_1', 'image_2')
class EditsheepMot(forms.ModelForm):
    class Meta:
        model = SheepMortality
        fields = ('mortality', 'location', 'ram_num', 'ewe_num', 'lamb', 'section', 'size', 'comment', 'image_1', 'image_2')

class EditpigMot(forms.ModelForm):
    class Meta:
        model = PigMortality
        fields = ('mortality', 'location', 'sow_num', 'boar_num', 'pigglet', 'section', 'size', 'comment', 'image_1', 'image_2')

class EditcowCull(forms.ModelForm):
    class Meta:
        model = CowCulling
        fields =('cow_num', 'bull_num', 'section', 'location', 'reason')

class EditsheepCull(forms.ModelForm):
    class Meta:
        model =  SheepCulling
        fields =('ewe_num', 'ram_num', 'section', 'location', 'reason')

class EditpigCull(forms.ModelForm):
    class Meta:
        model = PigCulling
        fields =('sow_num', 'boar_num', 'section', 'location', 'reason')

class EditgoatCull(forms.ModelForm):
    class Meta:
        model = GoatCulling
        fields =('doe_num', 'buck_num', 'section', 'location', 'reason')


class EditcowProc(forms.ModelForm):
    class Meta:
        model = CowProcurement
        fields = ('cow_num', 'size', 'bull_num', 'size1', 'section' )

class EditpigProc(forms.ModelForm):
    class Meta:
        model = PigProcurement
        fields = ('sow_num', 'size', 'boar_num', 'size1', 'section' )

class EditsheepProc(forms.ModelForm):
    class Meta:
        model = SheepProcurement
        fields = ('ewe_num', 'size', 'ram_num', 'size1', 'section' )

class EditgoatProc(forms.ModelForm):
    class Meta:
        model = GoatProcurement
        fields = ('buck_num', 'size', 'doe_num', 'size1', 'section' )


class EditcowSale(forms.ModelForm):
    class Meta:
        model = CowSale
        fields = fields =('cow_num', 'size', 'bull_num', 'size1', 'section', 'weight', 'price')

class EditgoatSale(forms.ModelForm):
    class Meta:
        model = GoatSale
        fields =('doe_num', 'size', 'buck_num', 'size1', 'section', 'weight', 'price')

class EditpigSale(forms.ModelForm):
    class Meta:
        model = PigSale
        fields =('sow_num', 'size', 'boar_num', 'size1', 'section', 'weight', 'price')

class EditsheepSale(forms.ModelForm):
    class Meta:
        model = SheepSale
        fields =('ewe_num', 'size', 'ram_num', 'size1', 'section', 'weight', 'price')
        
    
class CowmotFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = CowMortality
        fields =('date',)
        
class SheepmotFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = SheepMortality
        fields =('date',)

class GoatmotFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = GoatMortality
        fields =('date',)

class PigmotFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = PigMortality
        fields =('date',)


class PigcullFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = PigCulling
        fields =('date',)

class GoatcullFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = GoatCulling
        fields =('date',)

class SheepcullFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = SheepCulling
        fields =('date',)

class CowcullFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = CowCulling
        fields =('date',)

class CowsaleFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = CowSale
        fields =('date',)

class PigsaleFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = PigSale
        fields =('date',)

class GoatsaleFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = GoatSale
        fields =('date',)

class SheepsaleFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = SheepSale
        fields =('date',)

class CowprocFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = CowProcurement
        fields =('date',)

class PigprocFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = PigProcurement
        fields =('date',)

class SheepprocFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = SheepProcurement
        fields =('date',)

class GoatprocFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = GoatProcurement
        fields =('date',)