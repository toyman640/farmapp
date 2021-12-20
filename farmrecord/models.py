from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name='First name')
    last_name = models.CharField(max_length=100, verbose_name='Last name')
    email = models.EmailField(max_length=100, verbose_name='Email')

    def __str__(self):
        return self.user.username
class Section(models.Model):
    sec_name = models.CharField(max_length=100, verbose_name='Section Name')
    sec_desc = models.TextField(blank=True, verbose_name='Description')
    
    def __str__(self):
        return self.sec_name
    class Meta():
        verbose_name_plural='Section'


class CowMortality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mortality = models.CharField(max_length=10, verbose_name='mortality')
    date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200, verbose_name='loaction(s)')
    cow_num = models.IntegerField(verbose_name='Cow(s)', blank=True)
    bull_num = models.IntegerField(verbose_name='Bull(s)', blank=True)
    calves = models.IntegerField(verbose_name='calve(s)', blank=True)
    section = models.ManyToManyField(Section, verbose_name='Section')
    size = models.CharField(max_length=100, verbose_name='Size(s)')
    comment = models.TextField(max_length=500, verbose_name='comment' , blank=True)
    image_1 = models.FileField(verbose_name='first image', blank=True, null=True, upload_to='uploads/',)
    image_2 = models.FileField(verbose_name=' second image', blank=True, null=True, upload_to='uploads/')

    def __str__(self):
        return self.date

    def post_img(self):
        if self.pst_image:
          return self.pst_image_1.url
    
    def post_img1(self):
        if self.pst_image1:
          return self.pst_image2.url
    
    class Meta():
        verbose_name_plural='Cow mortality'


            
