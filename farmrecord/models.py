from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from farmapp.utils import unique_slug_generator
from django.db.models.signals import pre_save
from .validators import validate_file_size

# Create your models here.

class Userp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_boss = models.BooleanField('Is boss', default=False)
    is_hr = models.BooleanField('Is hr', default=False)
    is_supervisor = models.BooleanField('Is supervisor', default=False)
    is_account = models.BooleanField('Is account', default=False)
    is_maintenance = models.BooleanField('Is maintenance', default=False)
    is_drug = models.BooleanField("Is drug", default=False)
    is_vet = models.BooleanField('Is vet', default=False)
    is_vet_piggery = models.BooleanField('Is vet piggery', default=False)
    is_vet_paddock = models.BooleanField('Is vet cattle', default=False)
    is_vet_smallruminant = models.BooleanField('Is vet small ruminant', default=False)


class Animals(models.Model):
    ANIMAL_CHOICES = [
        ('pig', 'Pig'),
        ('cattle', 'Cattle'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
    ]
    animal_name = models.CharField(max_length=20, choices=ANIMAL_CHOICES, unique=True)
    describe_animal = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.animal_name


class AnimalType(models.Model):
    ANIMAL_TYPE_CHOICES = [
        ('sow', 'Sow'),
        ('boar', 'Boar'),
        ('weaner_pig', 'Weaner(Pig)'),
        ('piglet', 'Piglet'),
        ('cow', 'Cow'),
        ('bull', 'Bull'),
        ('weaner_cattle', 'Weaner(Cattle)'),
        ('calf', 'Calf'),
        ('ewe', 'Ewe'),
        ('ram', 'Ram'),
        ('weaner_sheep', 'Weaner(Sheep)'),
        ('lamb', 'Lamb'),
        ('buck', 'Buck'),
        ('doe', 'Doe'),
        ('weaner_goat', 'Weaner(Goat)'),
        ('kid', 'Kid'),
    ]
    animal = models.ForeignKey(Animals, on_delete=models.CASCADE, related_name="animal_types")
    animal_type_name = models.CharField(max_length=30, choices=ANIMAL_TYPE_CHOICES, unique=True)
    animal_type_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.animal_type_name


# class EventType(models.Model):
#     EVENT_CHOICES = [
#         ('mortality', 'Mortality'),
#         ('farrowing', 'Farrowing'),
#         ('calving', 'Calving'),
#         ('lambing', 'Lambing'),
#         ('kidding', 'Kidding'),
#         ('procurement', 'Procurement'),
#         ('culling', 'Culling'),
#         ('sale', 'Sale'),
#     ]
#     animal = models.ForeignKey(Animals, on_delete=models.CASCADE, related_name="events", null=True, blank=True)
#     animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name="events", null=True, blank=True)
#     event_name = models.CharField(max_length=20, choices=EVENT_CHOICES, unique=True)
#     location = models.CharField(max_length=100, null=True, blank=True)
#     designation = models.TextField(max_length=500, null=True, blank=True)
#     notes = models.TextField(null=True, blank=True)  # renamed from event_description

#     def __str__(self):
#         return self.event_name


class EventType(models.Model):
    EVENT_CHOICES = [
        ('mortality', 'Mortality'),
        ('farrowing', 'Farrowing'),
        ('calving', 'Calving'),
        ('lambing', 'Lambing'),
        ('kidding', 'Kidding'),
        ('procurement', 'Procurement'),
        ('culling', 'Culling'),
        ('sale', 'Sale'),
    ]

    # 🔹 Piggery Locations: Line + Block (A–Z)
    PIGGERY_LINES = [f"Line {i}" for i in range(1, 10)]
    PIGGERY_BLOCKS = [f"Block {chr(j)}" for j in range(65, 91)]  # A–Z
    PIGGERY_PENS = [f"Pen {i}" for i in range(1, 101)]  # 1–100

    PADDOCK_LOCATIONS = [(f"Paddock {i}", f"Paddock {i}") for i in range(1, 9)] + [
        ('Isolation', 'Isolation')
    ]
    SMALL_RUMINANT_LOCATIONS = [(f"Ewe {i}", f"Ewe {i}") for i in range(1, 6)]

    LOCATION_CHOICES = {
        'cattle': PADDOCK_LOCATIONS,
        'sheep': SMALL_RUMINANT_LOCATIONS,
        'goat': SMALL_RUMINANT_LOCATIONS,
    }

    animal = models.ForeignKey('Animals', on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    animal_type = models.ForeignKey('AnimalType', on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    event_name = models.CharField(max_length=20, choices=EVENT_CHOICES)
    location = models.CharField(max_length=100, null=True, blank=True)
    number_of_animals = models.PositiveIntegerField(default=1)
    designation = models.TextField(max_length=500, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.event_name

    def get_location_choices(self):
        """Return proper location list based on animal type"""
        if not self.animal_type or not self.animal_type.animal:
            return []
        key = self.animal_type.animal.animal_name.lower()
        return self.LOCATION_CHOICES.get(key, [])

class EventImage(models.Model):
    event = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='uploads/', validators=[validate_file_size], blank=True, null=True)  # Added validation
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for event: {self.event.event_name}"
