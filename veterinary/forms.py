# from django import forms
# from farmrecord.models import EventType, AnimalType, Animals


# class EventForm(forms.ModelForm):
#     image = forms.ImageField(required=False)

#     class Meta:
#         model = EventType
#         fields = [
#             'animal', 'animal_type', 'event_name',
#             'location', 'designation', 'notes', 'image'
#         ]

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         # Styling
#         self.fields['image'].widget.attrs.update({'class': 'form-control'})
#         self.fields['designation'].widget.attrs.update({'class': 'form-control', 'id': 'id_designation'})
#         self.fields['notes'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter notes...'})

#         # 🐖 VET PIGGERY
#         if user and getattr(user.profile, 'is_vet_piggery', False):
#             pig = Animals.objects.filter(animal_name='pig').first()
#             self.fields['animal'].initial = pig
#             self.fields['animal'].widget = forms.HiddenInput()
#             self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=pig)
#             self.fields['event_name'].choices = [('', '--- Select Event ---')] + [
#                 ('mortality', 'Mortality'),
#                 ('farrowing', 'Farrowing'),
#                 ('procurement', 'Procurement'),
#                 ('culling', 'Culling'),
#                 ('sale', 'Sale'),
#             ]

#         # 🐄 VET PADDOCK
#         elif user and getattr(user.profile, 'is_vet_paddock', False):
#             cattle = Animals.objects.filter(animal_name='cattle').first()
#             self.fields['animal'].initial = cattle
#             self.fields['animal'].widget = forms.HiddenInput()
#             self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=cattle)
#             self.fields['event_name'].choices = [('', '--- Select Event ---')] + [
#                 ('mortality', 'Mortality'),
#                 ('calving', 'Calving'),
#                 ('procurement', 'Procurement'),
#                 ('culling', 'Culling'),
#                 ('sale', 'Sale'),
#             ]

#         # 🐑🐐 SMALL RUMINANT
#         elif user and getattr(user.profile, 'is_vet_smallruminant', False):
#             sheep_goat = Animals.objects.filter(animal_name__in=['sheep', 'goat'])
#             self.fields['animal'].queryset = sheep_goat
#             self.fields['animal_type'].queryset = AnimalType.objects.filter(animal__in=sheep_goat)
#             self.fields['event_name'].choices = [('', '--- Select Event ---')] + [
#                 ('mortality', 'Mortality'),
#                 ('lambing', 'Lambing'),
#                 ('kidding', 'Kidding'),
#                 ('procurement', 'Procurement'),
#                 ('culling', 'Culling'),
#                 ('sale', 'Sale'),
#             ]

#         else:
#             self.fields['animal_type'].queryset = AnimalType.objects.all()
#             self.fields['event_name'].choices = EventType.EVENT_CHOICES

#         # Label for animal_type
#         self.fields['animal_type'].label_from_instance = (
#             lambda obj: dict(AnimalType.ANIMAL_TYPE_CHOICES).get(obj.animal_type_name, obj.animal_type_name)
#         )
from django import forms
from farmrecord.models import EventType, AnimalType, Animals


class EventForm(forms.ModelForm):
    image = forms.ImageField(required=False)
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

        # ✅ Required fields
        for field_name, field in self.fields.items():
            if field_name not in ['designation', 'notes', 'image']:
                field.required = True
            else:
                field.required = False

        for field in ['designation', 'notes', 'location', 'image']:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['designation'].widget.attrs.update({'id': 'id_designation'})
        self.fields['notes'].widget.attrs.update({'placeholder': 'Enter notes...'})

        # Detect section
        vet_section = None
        if user:
            if getattr(user.profile, 'is_vet_piggery', False):
                vet_section = 'pig'
            elif getattr(user.profile, 'is_vet_paddock', False):
                vet_section = 'cattle'
            elif getattr(user.profile, 'is_vet_smallruminant', False):
                vet_section = 'sheep'

        # Filter event and location choices based on section
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

            # ✅ Location choices per animal type
            if vet_section == 'pig':
                # Hide normal location for pigs (handled via JS)
                self.fields['location'].widget = forms.HiddenInput()
            elif vet_section == 'cattle':
                self.fields['location'].choices = [('', '--- Select Location ---')] + EventType.PADDOCK_LOCATIONS
            elif vet_section in ['sheep', 'goat']:
                self.fields['location'].choices = [('', '--- Select Location ---')] + EventType.SMALL_RUMINANT_LOCATIONS
        else:
            # Generic fallback
            self.fields['animal_type'].queryset = AnimalType.objects.all()
            self.fields['event_name'].choices = EventType.EVENT_CHOICES
            self.fields['location'].choices = [('', '--- Select Location ---')] + EventType.PADDOCK_LOCATIONS

        # Hide label if hidden input
        if isinstance(self.fields['animal'].widget, forms.HiddenInput):
            self.fields['animal'].label = ''
