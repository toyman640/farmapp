from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from farmapp.utils import unique_slug_generatorN


class Notification(models.Model):
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True)

def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notification.objects.create(user=kwargs.get('instance'), title='Welcome to our site!', message='Thanks')




def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generatorN(instance, instance.title, instance.slug)

pre_save.connect(slug_save, sender=Notification)