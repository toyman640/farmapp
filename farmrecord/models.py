from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name='First name')
    last_name = models.CharField(max_length=100, verbose_name='Last name')
    email = models.EmailField(max_length=100, verbose_name='Email')

    def __str__(self):
        return self.user.username

class CowRecords(models.Model):
    cow_ent = models.CharField(max_length=100, verbose_name='entry type')
    cow_desc = models.TextField(blank=True, null=True, verbose_name='Description')

    def __str__(self):
        return (self).cow_ent

    class Meta():
        verbose_name_plural = 'Cow Records'

class SheepRecords(models.Model):
    sheep_ent = models.CharField(max_length=100, verbose_name='entry type')
    sheep_desc = models.TextField(blank=True, null=True, verbose_name='Description')
     
    def __str__(self):
        return (self).sheep_ent

    class Meta():
        verbose_name_plural = 'Sheep Records'

class PigRecords(models.Model):
    pig_ent = models.CharField(max_length=100, verbose_name='entry type')
    pig_desc = models.TextField(blank=True, null=True, verbose_name='Description')

    def __str__(self):
        return (self).pig_ent

    class Meta():
        verbose_name_plural = 'Pig Records'

class GoatRecords(models.Model):
    goat_ent = models.CharField(max_length=100, verbose_name='entry type')
    goat_desc = models.TextField(blank=True, null=True, verbose_name='Description')

    def __str__(self):
        return (self).goat_ent
    class Meta():
        verbose_name_plural = 'Goat Records'