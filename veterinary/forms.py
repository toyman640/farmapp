from django import forms
from farmrecord.models import EventType, AnimalType, Animals, Census, CensusRecord
from django.forms import inlineformset_factory, BaseInlineFormSet


class EventForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    number_of_animals = forms.IntegerField(
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of animals'})
    )

    class Meta:
        model = EventType
        fields = [
            'animal', 'animal_type', 'event_name',
            'location', 'number_of_animals',
            'designation', 'notes', 'image'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Required and widget classes
        for field_name, field in self.fields.items():
            if field_name not in ['designation', 'notes', 'image']:
                field.required = True
            else:
                field.required = False
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['notes'].widget.attrs.update({'placeholder': 'Enter notes...'})

        # Detect vet section
        vet_section = None
        if user:
            if getattr(user.profile, 'is_vet_piggery', False):
                vet_section = 'pig'
            elif getattr(user.profile, 'is_vet_paddock', False):
                vet_section = 'cattle'
            elif getattr(user.profile, 'is_vet_smallruminant', False):
                vet_section = 'sheep'

        # Section-specific settings
        if vet_section:
            animal_obj = Animals.objects.filter(animal_name=vet_section).first()
            if animal_obj:
                self.fields['animal'].initial = animal_obj
                self.fields['animal'].widget = forms.HiddenInput()
                self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=animal_obj)

            section_events = {
                'pig': [('mortality', 'Mortality'), ('farrowing', 'Farrowing'),
                        ('procurement', 'Procurement'), ('culling', 'Culling'), ('sale', 'Sale')],
                'cattle': [('mortality', 'Mortality'), ('calving', 'Calving'),
                           ('procurement', 'Procurement'), ('culling', 'Culling'), ('sale', 'Sale')],
                'sheep': [('mortality', 'Mortality'), ('lambing', 'Lambing'),
                          ('kidding', 'Kidding'), ('procurement', 'Procurement'),
                          ('culling', 'Culling'), ('sale', 'Sale')],
            }

            self.fields['event_name'].choices = [('', '--- Select Event ---')] + section_events.get(vet_section, [])

            # Location setup
            if vet_section == 'pig':
                self.fields['location'].required = False
                self.fields['location'].widget = forms.HiddenInput()
            elif vet_section == 'cattle':
                self.fields['location'].choices = [('', '--- Select Location ---')] + EventType.PADDOCK_LOCATIONS
            elif vet_section in ['sheep', 'goat']:
                self.fields['location'].choices = [('', '--- Select Location ---')] + EventType.SMALL_RUMINANT_LOCATIONS
        else:
            self.fields['animal_type'].queryset = AnimalType.objects.all()
            self.fields['event_name'].choices = EventType.EVENT_CHOICES
            self.fields['location'].choices = [('', '--- Select Location ---')] + EventType.PADDOCK_LOCATIONS

        # Hide label if hidden
        if isinstance(self.fields['animal'].widget, forms.HiddenInput):
            self.fields['animal'].label = ''


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
                    animal_type_name__in=['boar', 'sow', 'weaner_pig', 'piglet']
                )
            elif getattr(user.profile, 'is_vet_paddock', False):
                self.fields['animal_type'].queryset = AnimalType.objects.filter(
                    animal__animal_name__iexact='cattle',
                    animal_type_name__in=['bull', 'cow', 'weaner_cattle', 'calf']
                )
            elif getattr(user.profile, 'is_vet_smallruminant', False):
                self.fields['animal_type'].queryset = AnimalType.objects.filter(
                    animal__animal_name__in=['sheep', 'goat'],
                    animal_type_name__in=['ram', 'ewe', 'weaner_sheep', 'buck', 'doe', 'weaner_goat', 'kid']
                )
            else:
                self.fields['animal_type'].queryset = AnimalType.objects.none()


# ✅ Custom inline formset that accepts user
class BaseCensusRecordFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user
        return super()._construct_form(i, **kwargs)


CensusRecordFormSet = inlineformset_factory(
    Census,
    CensusRecord,
    form=CensusRecordForm,
    formset=BaseCensusRecordFormSet,
    extra=4,
    can_delete=True
)