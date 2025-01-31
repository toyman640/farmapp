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


class Animals(models.Model):
    animal_name = models.CharField(max_length=50)
    describe_animal = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.animal_name


class AnimalType(models.Model):
    animal = models.ForeignKey(Animals, on_delete=models.CASCADE, related_name="animal_types")
    animal_type_name = models.CharField(max_length=200)
    animal_type_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.animal_type_name


class EventType(models.Model):
    animal = models.ForeignKey(Animals, on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    event_name = models.CharField(max_length=200)
    event_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.event_name  # Fixed the incorrect field reference


class EventImage(models.Model):
    event = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='uploads/', validators=[validate_file_size])  # Added validation
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for event: {self.event.event_name}"
