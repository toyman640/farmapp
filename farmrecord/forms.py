from cProfile import label
from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from farmrecord.models import *
from humanR.models import *
from django.core import validators
from notification.models import Notification


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
        fields = ('mortality', 'location', 'sow_num', 'boar_num', 'nursing_num', 'hogs_num', 'growers_num', 'weaners_num', 'drysows_num', 'section', 'size', 'comment','pigglet', 'commentp','image_1', 'image_2')
        labels = {
            "comment" : "Cause of mortality"
        }

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
        fields =('cow_num', 'size', 'price', 'bull_num', 'size1', 'price1', 'section', 'weight', 'total_price')

class GoatsaleForm(forms.ModelForm):
    class Meta:
        model = GoatSale
        fields =('doe_num', 'size', 'price', 'buck_num', 'size1', 'price1' ,'section', 'weight', 'total_price')

class SheepsaleForm(forms.ModelForm):
    class Meta:
        model = SheepSale
        fields =('ewe_num', 'size', 'price', 'ram_num', 'size1', 'price1', 'section', 'weight', 'total_price')

class PigsaleForm(forms.ModelForm):
    class Meta:
        model = PigSale
        fields =('sow_num', 'size', 'price', 'boar_num', 'size1', 'price1', 'section', 'weight', 'total_price')

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

class CowCen(forms.ModelForm):
    class Meta:
        model = CowCensusPop
        fields = ('month', 'cow_population', 'bull_population', 'calf_population')

class GoatCen(forms.ModelForm):
    class Meta:
        model = GoatCensusPop
        fields = ('month', 'doe_population', 'buck_population', 'kid_population')

class PigCen(forms.ModelForm):
    class Meta:
        model = PigCensusPop
        fields = ('month', 'sow_population', 'boar_population', 'hog_population', 'weaner_population', 'grower_population', 'dry_population')

class SheepCen(forms.ModelForm):
    class Meta:
        model = SheepCensusPop
        fields = ('month', 'ewe_population', 'ram_population', 'lamb_population')

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
        fields = fields =('cow_num', 'size', 'price' ,'bull_num', 'size1', 'price1' ,'section', 'weight', 'total_price')

class EditgoatSale(forms.ModelForm):
    class Meta:
        model = GoatSale
        fields =('doe_num', 'size', 'price' ,'buck_num', 'size1', 'price1' ,'section', 'weight', 'total_price')

class EditpigSale(forms.ModelForm):
    class Meta:
        model = PigSale
        fields =('sow_num', 'size', 'price' ,'boar_num', 'size1', 'price1' ,'section', 'weight', 'total_price')

class EditsheepSale(forms.ModelForm):
    class Meta:
        model = SheepSale
        fields =('ewe_num', 'size', 'price' ,'ram_num', 'size1', 'price1' ,'section', 'weight', 'total_price')
        
    
class CowmotFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = CowMortality
        fields =('date','export_to_CSV')
        
class SheepmotFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = SheepMortality
        fields =('date','export_to_CSV')

class GoatmotFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = GoatMortality
        fields =('date','export_to_CSV')

class PigmotFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = PigMortality
        fields =('date','export_to_CSV')


class PigcullFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = PigCulling
        fields =('date','export_to_CSV')

class GoatcullFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = GoatCulling
        fields =('date','export_to_CSV')

class SheepcullFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))

    class Meta:
        model = SheepCulling
        fields =('date','export_to_CSV')

class CowcullFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = CowCulling
        fields =('date','export_to_CSV')

class CowsaleFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = CowSale
        fields =('date','export_to_CSV')

class PigsaleFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = PigSale
        fields =('date','export_to_CSV')

class GoatsaleFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = GoatSale
        fields =('date','export_to_CSV')

class SheepsaleFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = SheepSale
        fields =('date','export_to_CSV')

class CowprocFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = CowProcurement
        fields =('date','export_to_CSV')

class PigprocFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = PigProcurement
        fields =('date','export_to_CSV')

class SheepprocFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = SheepProcurement
        fields =('date','export_to_CSV')

class GoatprocFilter(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), required=False)
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'From'}))
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type' : 'date', 'placeholder': 'To'}))
    export_to_CSV = forms.BooleanField(required=False, label="Export to CSV")

    class Meta:
        model = GoatProcurement
        fields =('date','export_to_CSV')

class RemarkForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
       
    # message = forms.CharField(label='Message', widget=forms.TextInput(
    #     attrs={'class': 'form-control'}))
    user = forms.ModelChoiceField(label='Send to',queryset=User.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}))    
    class Meta:
        model = Notification
        fields = ('title', 'message', 'user')

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('title_id', 'job_desc', 'section_id', 'employee_SN', 'employee_FN', 'employee_MN', 'address', 'phone', 'sex', 'age', 'bank_num', 'bank_name', 'bvn', 'email', 'id_type', 'id_num', 'signed', 'nok_surname', 'nok_oname', 'nok_address', 'nok_phone', 'nok_relationship', 'guarantor', 'signed', 'verified', 'image_1')
        exclude = ['date']

class EmployeeFilter(forms.ModelForm):
    employee_SN = forms.CharField(required=False, label= 'Surname',  widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Surname'}))
    employee_FN = forms.CharField(required=False , label='First name' )
    section_id = forms.ModelChoiceField(label='Section' ,queryset=FarmSection.objects.all(), required=False)
    title_id = forms.ModelChoiceField(label='Job title', queryset=JobTitle.objects.all(), required=False)
    class Meta:
        model = Employee
        fields = ('section_id', 'title_id', 'employee_SN', 'employee_FN') 

class EditempRec(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('title_id', 'job_desc', 'section_id', 'employee_SN', 'employee_FN', 'employee_MN', 'address', 'phone', 'sex', 'age', 'bank_num', 'bank_name', 'bvn', 'email', 'id_type', 'id_num', 'signed', 'nok_surname', 'nok_oname', 'nok_address', 'nok_phone', 'nok_relationship', 'guarantor', 'signed', 'verified', 'image_1')


class CowBirthForm(forms.ModelForm):
    class Meta:
        model = CowBirth
        fields = ('section', 'clavings_num', 'claves_num', 'still_birthc','weak_claves', 'defected_calf', 'comment_c' )


class SheepBirthForm(forms.ModelForm):
    class Meta:
        model = SheepBirth
        fields = ('section', 'lambings_num', 'lambs_num', 'still_births','weak_lamb', 'defected_lamb', 'comment_s' )


class PigBirthForm(forms.ModelForm):
    class Meta:
        model = PigBirth
        fields = ('section', 'farrowing_num', 'pigglets_num', 'still_birthp','weak_pigglet', 'defected_pigglet','devoured_pigglet','overlaying', 'comment_p' )


class GoatBirthForm(forms.ModelForm):
    class Meta:
        model = GoatBirth
        fields = ('section', 'kiddings_num', 'kids_num', 'still_birthg','weak_kid', 'defected_kid', 'comment_g' )


