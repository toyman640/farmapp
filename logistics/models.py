from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from autoslug import AutoSlugField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    description = models.TextField(max_length=500, verbose_name='Description' , blank=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    motor_name = models.CharField(max_length=100, verbose_name='name')
    motor_desc = models.TextField(max_length=500, verbose_name='Description of the Vehicle', blank=True, null=True)
    motor_image1 = models.ImageField(verbose_name='Vehicle Image', blank=True, null=True)
    motor_image2 = models.ImageField(verbose_name='Vehicle Image 2', blank=True, null=True)


    def __str__(self):
        return self.motor_name



class Feed(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cat_name1 = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    truck = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name='Truck')
    item = models.TextField(max_length=100, verbose_name='Item')
    checkout = models.CharField(max_length=100, verbose_name='Place')
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.item)
        super(Feed, self).save(*args, **kwargs)


    def __str__(self):
        return self.cat_name1


class Diesel(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cat_name3 = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category')
    motor = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    desc = models.TextField(max_length=500, verbose_name='Description', null=True, blank=True)
    liters = models.IntegerField( verbose_name='Liters', default=0)
    location = models.CharField(max_length=100, verbose_name='Location')
    price = models.IntegerField( verbose_name='Amount', default=0)
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.motor)
        super(Diesel, self).save(*args, **kwargs)



    def __str__(self):
        return str(self.cat_name3)


class Maintenance(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cat_name4 = models.ForeignKey(Category, on_delete=models.CASCADE)
    items = models.CharField(max_length=100, verbose_name='Parts Repaired')
    price = models.IntegerField(verbose_name='Amount')
    t_price = models.IntegerField(verbose_name='Total Amount')

    def __str__(self):
        return self.cat_name4
