from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    description = models.TextField(max_length=500, verbose_name='Description' , blank=True)

    def __str__(self):
        return self.name



class Feed(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cat_name1 = models.ForeignKey(Category, on_delete=models.CASCADE)
    truck = models.CharField(max_length=100, verbose_name='Truck Number')
    item = models.CharField(max_length=100, verbose_name='Item')
    checkout = models.CharField(max_length=100, verbose_name='Place')
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.feed_truck)
        super(Feed, self).save(*args, **kwargs)


    def __str__(self):
        return self.cat_name1


class Diesel(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cat_name3 = models.ForeignKey(Category, on_delete=models.CASCADE)
    motor = models.CharField(max_length=100, verbose_name='Motor')
    liters = models.IntegerField( verbose_name='Liters', default=0)
    location = models.CharField(max_length=100, verbose_name='Location')
    price = models.IntegerField( verbose_name='Amount', default=0)
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.diesel_motor)
        super(Diesel, self).save(*args, **kwargs)


    def __str__(self):
        return self.cat_name3
