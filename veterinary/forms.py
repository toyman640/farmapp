from django import forms
from farmrecord.models import EventType, AnimalType, Animals


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
