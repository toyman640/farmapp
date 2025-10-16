
# # from django import forms
# # from .models import Animals, AnimalType, EventType, EventImage

# # class AnimalsForm(forms.ModelForm):
# #     class Meta:
# #         model = Animals
# #         fields = ['animal_name', 'describe_animal']
# #         widgets = {
# #             'animal_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter animal name'}),
# #             'describe_animal': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the animal'}),
# #         }


# # class AnimalTypeForm(forms.ModelForm):
# #     class Meta:
# #         model = AnimalType
# #         fields = ['animal', 'animal_type_name', 'animal_type_description']
# #         widgets = {
# #             'animal': forms.Select(attrs={'class': 'form-control'}),
# #             'animal_type_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter animal type name'}),
# #             'animal_type_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the animal type'}),
# #         }


# # class EventTypeForm(forms.ModelForm):
# #     class Meta:
# #         model = EventType
# #         fields = ['animal', 'animal_type', 'event_name', 'event_description']
# #         widgets = {
# #             'animal': forms.Select(attrs={'class': 'form-control'}),
# #             'animal_type': forms.Select(attrs={'class': 'form-control'}),
# #             'event_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event name'}),
# #             'event_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the event'}),
# #         }


# # class EventImageForm(forms.ModelForm):
# #     class Meta:
# #         model = EventImage
# #         fields = ['event', 'image']
# #         widgets = {
# #             'event': forms.Select(attrs={'class': 'form-control'}),
# #             'image': forms.ClearableFileInput(attrs={'multiple': False, 'class': 'form-control'}),
# #         }


# from django import forms
# from .models import EventType, EventImage, AnimalType, Animals


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
