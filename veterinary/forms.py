from django import forms
from farmrecord.models import EventType, AnimalType, Animals, Census, CensusRecord, PiggeryCensusRecord, PiggeryLine
from django.forms import inlineformset_factory, BaseInlineFormSet, modelformset_factory
from django.utils import timezone


class EventBaseForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=timezone.now().date()
    )

    class Meta:
        model = EventType
        fields = ['animal', 'animal_type', 'event_name', 'event_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        vet_section = None
        if user:
            if getattr(user.profile, 'is_vet_piggery', False):
                vet_section = 'pig'
            elif getattr(user.profile, 'is_vet_paddock', False):
                vet_section = 'cattle'
            elif getattr(user.profile, 'is_vet_smallruminant', False):
                vet_section = 'sheep'

        if vet_section:
            animal_obj = Animals.objects.filter(animal_name=vet_section).first()
            if animal_obj:
                self.fields['animal'].initial = animal_obj
                self.fields['animal'].widget = forms.HiddenInput()
                self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=animal_obj)

            section_events = {
                'pig': [('castration', 'Castration'), ('culling', 'Culling'), ('farrowing', 'Farrowing'),
                        ('gift', 'Gift'), ('mortality', 'Mortality'), ('procurement', 'Procurement'), ('sale', 'Sale'), ('treatment', 'Treatment')],
                'cattle': [('calving', 'Calving'), ('culling', 'Culling'),
                           ('gift', 'Gift'), ('mortality', 'Mortality'),('other', 'Other (Describe in notes)'),('procurement', 'Procurement'), ('sale', 'Sale'), ('treatment', 'Treatment'), ('vaccination', 'Vaccination')],
                'sheep': [('culling', 'Culling'), ('gift', 'Gift'), ('kidding', 'Kidding'),
                          ('lambing', 'Lambing'), ('mortality', 'Mortality'), ('procurement', 'Procurement'),
                          ('sale', 'Sale'), ('treatment', 'Treatment'), ('vaccination', 'Vaccination')],
            }
            self.fields['event_name'].choices = [('', '--- Select Event ---')] + section_events.get(vet_section, [])
        else:
            self.fields['animal_type'].queryset = AnimalType.objects.all()
            self.fields['event_name'].choices = EventType.EVENT_CHOICES

        if isinstance(self.fields['animal'].widget, forms.HiddenInput):
            self.fields['animal'].label = ''


class EventDetailForm(forms.ModelForm):
    number_of_animals = forms.IntegerField(
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qty'})
    )

    # Add this field so it becomes available to crispy forms
    edit_note = forms.CharField(
        required=False, 
        label="Reason for Edit (Note to Admin)",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Explain why you are editing this record...'})
    )
    
    designation = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter notes...'}))
    location = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = EventType
        fields = ['location', 'number_of_animals', 'designation', 'notes']


EventDetailFormSet = modelformset_factory(
    EventType,
    form=EventDetailForm,
    extra=1,
    max_num=10,
    can_delete=True
)


# class EventForm(forms.ModelForm):
#     # image = forms.ImageField(
#     #     required=False,
#     #     widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
#     # )
#     number_of_animals = forms.IntegerField(
#         required=True,
#         min_value=1,
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of animals'})
#     )

#     edit_note = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'rows': 3,
#             'placeholder': 'Explain why this edit is needed...'
#         })
#     )

#     # ... existing fields
#     event_date = forms.DateField(
#         widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#         initial=timezone.now().date()
#     )

#     class Meta:
#         model = EventType
#         fields = [
#             'animal', 'animal_type', 'event_name', 'event_date',
#             'location', 'number_of_animals',
#             'designation', 'notes',
#         ]

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         edit_mode = kwargs.pop('edit_mode', False)
#         super().__init__(*args, **kwargs)
#         # if not edit_mode:
#         #     self.fields.pop('edit_note', None)
#         if not self.is_bound and self.instance.pk:
#             self.initial['location'] = self.instance.location

        
#         for field_name, field in self.fields.items():
#             if field_name not in ['designation', 'notes', 'image', 'edit_note', 'location']:
#                 field.required = True
#             else:
#                 field.required = False

#         if not edit_mode:
#             self.fields.pop('edit_note', None)
#         else:
#             self.fields['edit_note'].required = True
        

#         self.fields['notes'].widget.attrs.update({'placeholder': 'Enter notes...'})

#         # Detect vet section
#         vet_section = None
#         if user:
#             if getattr(user.profile, 'is_vet_piggery', False):
#                 vet_section = 'pig'
#             elif getattr(user.profile, 'is_vet_paddock', False):
#                 vet_section = 'cattle'
#             elif getattr(user.profile, 'is_vet_smallruminant', False):
#                 vet_section = 'sheep'

#         # Section-specific settings
#         if vet_section:
#             animal_obj = Animals.objects.filter(animal_name=vet_section).first()
#             if animal_obj:
#                 self.fields['animal'].initial = animal_obj
#                 self.fields['animal'].widget = forms.HiddenInput()
#                 self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=animal_obj)

#             section_events = {
#                 'pig': [('castration', 'Castration'), ('culling', 'Culling'), ('farrowing', 'Farrowing'),
#                         ('gift', 'Gift'), ('mortality', 'Mortality'), ('procurement', 'Procurement'), ('sale', 'Sale'), ('treatment', 'Treatment')],
#                 'cattle': [('calving', 'Calving'), ('culling', 'Culling'),
#                            ('gift', 'Gift'), ('mortality', 'Mortality'),('other', 'Other (Describe in notes)'),('procurement', 'Procurement'), ('sale', 'Sale'), ('treatment', 'Treatment'), ('vaccination', 'Vaccination')],
#                 'sheep': [('culling', 'Culling'), ('gift', 'Gift'), ('kidding', 'Kidding'),
#                           ('lambing', 'Lambing'), ('mortality', 'Mortality'), ('procurement', 'Procurement'),
#                           ('sale', 'Sale'), ('treatment', 'Treatment'), ('vaccination', 'Vaccination')],
#             }

#             self.fields['event_name'].choices = [('', '--- Select Event ---')] + section_events.get(vet_section, [])

#             # Location setup
#             if vet_section == 'pig':
#                 self.fields['location'].required = False
#                 self.fields['location'].widget = forms.HiddenInput()
#             elif vet_section == 'cattle':
#                 self.fields['location'].choices = [('', '--- Select Location ---')] + EventType.PADDOCK_LOCATIONS
#             elif vet_section in ['sheep', 'goat']:
#                 self.fields['location'].choices = [('', '--- Select Location ---')] + EventType.SMALL_RUMINANT_LOCATIONS
#         else:
#             self.fields['animal_type'].queryset = AnimalType.objects.all()
#             self.fields['event_name'].choices = EventType.EVENT_CHOICES
#             self.fields['location'].choices = [('', '--- Select Location ---')] + EventType.PADDOCK_LOCATIONS

#         # Hide label if hidden
#         if isinstance(self.fields['animal'].widget, forms.HiddenInput):
#             self.fields['animal'].label = ''


class CensusForm(forms.ModelForm):
    class Meta:
        model = Census
        fields = ['animal', 'census_date', 'notes']
        widgets = {
            'animal': forms.HiddenInput(),
            'census_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Prefill animal based on vet section
        if user:
            if getattr(user.profile, 'is_vet_piggery', False):
                animal_obj = Animals.objects.filter(animal_name__iexact='pig').first()
            elif getattr(user.profile, 'is_vet_paddock', False):
                animal_obj = Animals.objects.filter(animal_name__iexact='cattle').first()
            elif getattr(user.profile, 'is_vet_smallruminant', False):
                animal_obj = Animals.objects.filter(animal_name__in=['sheep', 'goat']).first()
            else:
                animal_obj = None

            if animal_obj:
                self.fields['animal'].initial = animal_obj


class CensusRecordForm(forms.ModelForm):
    class Meta:
        model = CensusRecord
        fields = ['animal_type', 'number_of_animals']
        widgets = {
            'number_of_animals': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        

        # Filter animal types by vet section
        if user:
            if getattr(user.profile, 'is_vet_piggery', False):
                self.fields['animal_type'].queryset = AnimalType.objects.filter(
                    animal__animal_name__iexact='pig',
                    animal_type_name__in=['boar', 'sow', 'weaner (pig)', 'piglet']
                )
            elif getattr(user.profile, 'is_vet_paddock', False):
                self.fields['animal_type'].queryset = AnimalType.objects.filter(
                    animal__animal_name__iexact='cattle',
                    animal_type_name__in=['bull', 'cow', 'weaner (cattle)', 'calf', 'miniature cattle', 'donkey']
                )
            elif getattr(user.profile, 'is_vet_smallruminant', False):
                self.fields['animal_type'].queryset = AnimalType.objects.filter(
                    animal__animal_name__in=['sheep', 'goat'],
                    animal_type_name__in=['ram', 'ewe', 'weaner (sheep)', 'lamb', 'buck', 'doe', 'weaner (goat)', 'kid']
                )
            else:
                self.fields['animal_type'].queryset = AnimalType.objects.none()


class BaseCensusRecordFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user
        return super()._construct_form(i, **kwargs)

    @property
    def empty_form(self):
        """Ensure empty_form also gets user context for filtered queryset"""
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            user=self.user,
            use_required_attribute=False,  # ✅ Prevent ValueError
        )
        self.add_fields(form, None)
        return form

CensusRecordFormSet = inlineformset_factory(
    Census,
    CensusRecord,
    form=CensusRecordForm,
    formset=BaseCensusRecordFormSet,
    extra=0,  # ✅ show 1 form initially
    min_num=1,  # ✅ at least 1
    validate_min=True,
    max_num=15,  # ✅ allow up to 15
    validate_max=True,
    can_delete=True
)


class PiggeryCensusRecordForm(forms.ModelForm):
    class Meta:
        model = PiggeryCensusRecord
        fields = ['line', 'number', 'total_piglets', 'note'] # Added total_piglets
        widgets = {
            'line': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_piglets': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        # Pop 'user' before calling super()
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

class BasePiggeryCensusRecordFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) # Pop user here
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user # Pass user to the form
        return super()._construct_form(i, **kwargs)

# Update your factory to use this formset class
PiggeryCensusRecordFormSet = inlineformset_factory(
    Census,
    PiggeryCensusRecord,
    form=PiggeryCensusRecordForm,
    formset=BasePiggeryCensusRecordFormSet, # <--- Ensure this is set
    extra=0,
    can_delete=True
)


class PiggeryLineForm(forms.ModelForm):
    class Meta:
        model = PiggeryLine
        fields = ['name', 'specification']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Line 1'}),
            'specification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Breeding'}),
        }