from django.dispatch import receiver
from django.db.models.signals import(
    post_save,
)
from django.contrib.auth.models import User
from farmrecord.models import Userp


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Userp.objects.create(
            user=instance
        )