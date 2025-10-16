from django import forms
from farmrecord.models import EventType, EventImage, AnimalType, Animals



class EventForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = EventType
        fields = [
            'animal', 'animal_type', 'event_name', 
            'location', 'designation', 'description', 
            'event_description', 'image'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs.update({'class': 'form-control'})

        # 🐖 VET PIGGERY
        if user and getattr(user.profile, 'is_vet_piggery', False):
            pig = Animals.objects.filter(animal_name='pig').first()
            self.fields['animal'].initial = pig
            self.fields['animal'].widget = forms.HiddenInput()
            self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=pig)
            self.fields['event_name'].choices = [
                ('mortality', 'Mortality'),
                ('farrowing', 'Farrowing'),
                ('procurement', 'Procurement'),
                ('culling', 'Culling'),
                ('sale', 'Sale'),
            ]

        # 🐄 VET PADDOCK (Cattle)
        elif user and getattr(user.profile, 'is_vet_paddock', False):
            cattle = Animals.objects.filter(animal_name='cattle').first()
            self.fields['animal'].initial = cattle
            self.fields['animal'].widget = forms.HiddenInput()
            self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=cattle)
            self.fields['event_name'].choices = [
                ('mortality', 'Mortality'),
                ('calving', 'Calving'),
                ('procurement', 'Procurement'),
                ('culling', 'Culling'),
                ('sale', 'Sale'),
            ]

        # 🐑🐐 VET SMALL RUMINANT (Sheep/Goat)
        elif user and getattr(user.profile, 'is_vet_smallruminant', False):
            sheep_goat = Animals.objects.filter(animal_name__in=['sheep', 'goat'])
            self.fields['animal'].queryset = sheep_goat
            self.fields['animal_type'].queryset = AnimalType.objects.filter(animal__in=sheep_goat)
            self.fields['event_name'].choices = [
                ('mortality', 'Mortality'),
                ('lambing', 'Lambing'),
                ('kidding', 'Kidding'),
                ('procurement', 'Procurement'),
                ('culling', 'Culling'),
                ('sale', 'Sale'),
            ]

        # 🧑‍⚕️ OTHER USERS — show all
        else:
            self.fields['animal_type'].queryset = AnimalType.objects.all()
            self.fields['event_name'].choices = EventType.EVENT_CHOICES

        # ✅ Display user-friendly labels for animal_type
        self.fields['animal_type'].label_from_instance = (
            lambda obj: dict(AnimalType.ANIMAL_TYPE_CHOICES).get(obj.animal_type_name, obj.animal_type_name)
        )


# class EventForm(forms.ModelForm):
#     image = forms.ImageField(required=False)

#     class Meta:
#         model = EventType
#         fields = ['animal', 'animal_type', 'event_name', 'location', 'designation', 'description', 'event_description', 'image']

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         self.fields['image'].widget.attrs.update({'class': 'form-control'})

#         # 🐖 Vet Piggery
#         if user and getattr(user.profile, 'is_vet_piggery', False):
#             pig = Animals.objects.filter(animal_name='pig').first()
#             self.fields['animal'].initial = pig
#             self.fields['animal'].widget = forms.HiddenInput()
#             self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=pig)

#         # 🐄 Vet Paddock (Cattle)
#         elif user and getattr(user.profile, 'is_vet_paddock', False):
#             cattle = Animals.objects.filter(animal_name='cattle').first()
#             self.fields['animal'].initial = cattle
#             self.fields['animal'].widget = forms.HiddenInput()
#             self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=cattle)

#         # 🐑 Small Ruminant (Sheep/Goat)
#         elif user and getattr(user.profile, 'is_vet_smallruminant', False):
#             sheep_goat = Animals.objects.filter(animal_name__in=['sheep', 'goat'])
#             self.fields['animal'].queryset = sheep_goat
#             self.fields['animal_type'].queryset = AnimalType.objects.filter(animal__in=sheep_goat)

#         # ✨ Set display label
#         self.fields['animal_type'].label_from_instance = lambda obj: dict(AnimalType.ANIMAL_TYPE_CHOICES).get(obj.animal_type_name, obj.animal_type_name)


# class EventForm(forms.ModelForm):
#     image = forms.ImageField(required=False)

#     class Meta:
#         model = EventType
#         fields = [
#             'animal',
#             'animal_type',
#             'event_name',
#             'location',
#             'designation',
#             'description',
#             'event_description',
#             'image',
#         ]

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         # Add Bootstrap styling to the image field
#         self.fields['image'].widget.attrs.update({'class': 'form-control'})

#         # Default queryset
#         self.fields['animal_type'].queryset = AnimalType.objects.all()

#         # 🧠 Handle vet-specific filtering
#         if user and hasattr(user, 'profile'):

#             # 🐷 VET PIGGERY
#             if user.profile.is_vet_piggery:
#                 pig = Animals.objects.filter(animal_name='pig').first()
#                 if pig:
#                     self.fields['animal'].initial = pig
#                     self.fields['animal'].widget = forms.HiddenInput()
#                     self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=pig)

#             # 🐄 VET PADDOCK (Cattle)
#             elif user.profile.is_vet_paddock:
#                 cattle = Animals.objects.filter(animal_name='cattle').first()
#                 if cattle:
#                     self.fields['animal'].initial = cattle
#                     self.fields['animal'].widget = forms.HiddenInput()
#                     self.fields['animal_type'].queryset = AnimalType.objects.filter(animal=cattle)

#             # 🐑🐐 SMALL RUMINANT VET (Sheep or Goat)
#             elif user.profile.is_vet_smallruminant:
#                 small_ruminants = Animals.objects.filter(animal_name__in=['sheep', 'goat'])
#                 self.fields['animal'].queryset = small_ruminants
#                 if small_ruminants.exists():
#                     self.fields['animal'].initial = small_ruminants.first()
#                 self.fields['animal_type'].queryset = AnimalType.objects.filter(animal__in=small_ruminants)

#             # 🧑‍⚕️ Other vets or general users — all animals and types remain available
#             else:
#                 self.fields['animal_type'].queryset = AnimalType.objects.all()
