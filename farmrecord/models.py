from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone

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
    mortality = models.CharField(max_length=10, verbose_name='mortality')
    date = models.DateTimeField(auto_now=False)
    location = models.CharField(max_length=200, verbose_name='loaction(s)')
    cow_num = models.IntegerField(verbose_name='Cow(s)', blank=True, null=True)
    bull_num = models.IntegerField(verbose_name='Bull(s)', blank=True, null=True)
    calves = models.IntegerField(verbose_name='calve(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category1', null=True, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, verbose_name='Size(s)')
    comment = models.TextField(max_length=500, verbose_name='Cause of death' , blank=True)
    image_1 = models.FileField(verbose_name='first image', blank=True, null=True, upload_to='uploads/',)
    image_2 = models.FileField(verbose_name=' second image', blank=True, null=True, upload_to='uploads/')

    def __str__(self):
        return self.location

    def post_img(self):
        if self.image_1:
          return self.image_1.url
    
    def post_img1(self):
        if self.image_2:
          return self.image_2.url
    
    class Meta():
        verbose_name_plural='Cow mortality'


class SheepMortality(models.Model):
    mortality = models.CharField(max_length=10, verbose_name='mortality')
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=200, verbose_name='loaction(s)')
    ewe_num = models.IntegerField(verbose_name='Ewe(s)', blank=True, null=True)
    ram_num = models.IntegerField(verbose_name='Ram(s)', blank=True, null=True)
    lamb = models.IntegerField(verbose_name='lamb(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category2', null=True, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, verbose_name='Size(s)')
    comment = models.TextField(max_length=500, verbose_name='Cause of death' , blank=True)
    image_1 = models.FileField(verbose_name='first image', blank=True, null=True, upload_to='uploads/',)
    image_2 = models.FileField(verbose_name=' second image', blank=True, null=True, upload_to='uploads/')

    def __str__(self):
        return self.location

    def post_img(self):
        if self.image_1:
          return self.image_1.url
    
    def post_img1(self):
        if self.image_2:
          return self.image_2.url
    
    class Meta():
        verbose_name_plural='Sheep mortality'


class GoatMortality(models.Model):
    mortality = models.CharField(max_length=10, verbose_name='mortality')
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=200, verbose_name='loaction(s)')
    doe_num = models.IntegerField(verbose_name='Doe(s)', blank=True, null=True)
    buck_num = models.IntegerField(verbose_name='Buck(s)', blank=True, null=True)
    kid = models.IntegerField(verbose_name='kid(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category3', null=True, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, verbose_name='Size(s)')
    comment = models.TextField(max_length=500, verbose_name='Cause of death' , blank=True)
    image_1 = models.FileField(verbose_name='first image', blank=True, null=True, upload_to='uploads/',)
    image_2 = models.FileField(verbose_name=' second image', blank=True, null=True, upload_to='uploads/')

    def __str__(self):
        return self.location

    def post_img(self):
        if self.image_1:
          return self.image_1.url
    
    def post_img1(self):
        if self.image_2:
          return self.image_2.url
    
    class Meta():
        verbose_name_plural='Goat mortality'

class PigMortality(models.Model):
    mortality = models.CharField(max_length=10, verbose_name='mortality')
    date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=200, verbose_name='loaction(s)')
    sow_num = models.IntegerField(verbose_name='Sow(s)', blank=True, null=True)
    boar_num = models.IntegerField(verbose_name='Boar(s)', blank=True, null=True)
    pigglet = models.IntegerField(verbose_name='Pigglet(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category4', null=True, on_delete=models.CASCADE)
    size = models.CharField(max_length=100, verbose_name='Size(s)')
    comment = models.TextField(max_length=500, verbose_name='Cause of death' , blank=True)
    image_1 = models.FileField(verbose_name='first image', blank=True, null=True, upload_to='uploads/',)
    image_2 = models.FileField(verbose_name=' second image', blank=True, null=True, upload_to='uploads/')

    def __str__(self):
        return self.location

    def post_img(self):
        if self.image_1:
          return self.image_1.url
    
    def post_img1(self):
        if self.image_2:
          return self.image_2.url
    
    class Meta():
        verbose_name_plural='Pig mortality'


class SheepCulling(models.Model):
    date = models.DateField(default=timezone.now)
    ewe_num = models.IntegerField(verbose_name='Ewe(s)', blank=True, null=True)
    ram_num = models.IntegerField(verbose_name='Ram(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category5', null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=500, verbose_name='Location(s)')
    reason = models.TextField(max_length=500, verbose_name='Reason', blank=True)

    def __str__(self):
        return self.reason          

class CowCulling(models.Model):
    date = models.DateField(default=timezone.now)
    cow_num = models.IntegerField(verbose_name='Cow(s)', blank=True, null=True)
    bull_num = models.IntegerField(verbose_name='Bull(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category6', null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=500, verbose_name='Location(s)')
    reason = models.TextField(max_length=500, verbose_name='Reason', blank=True)

    def __str__(self):
        return self.reason

class GoatCulling(models.Model):
    date = models.DateField(default=timezone.now)
    doe_num = models.IntegerField(verbose_name='Doe(s)', blank=True, null=True)
    buck_num = models.IntegerField(verbose_name='Buck(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category7', null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=500, verbose_name='Location(s)')
    reason = models.TextField(max_length=500, verbose_name='Reason', blank=True)

    def __str__(self):
        return self.reason         

class PigCulling(models.Model):
    date = models.DateField(default=timezone.now)
    sow_num = models.IntegerField(verbose_name='Sow(s)', blank=True, null=True)
    boar_num = models.IntegerField(verbose_name='Boar(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category8', null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=500, verbose_name='Location(s)')
    reason = models.TextField(max_length=500, verbose_name='Reason', blank=True)

    def __str__(self):
        return self.reason

class CowSale(models.Model):
    date = models.DateField(default=timezone.now)
    cow_num = models.IntegerField(verbose_name='Cow(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    bull_num = models.IntegerField(verbose_name='Bull(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category9', null=True, on_delete=models.CASCADE)
    weight= models.IntegerField(verbose_name='Weight(s)')
    price = models.IntegerField(verbose_name='Price(s)')

    def __str__(self):
        return self.price

class SheepSale(models.Model):
    date = models.DateField(default=timezone.now)
    ewe_num = models.IntegerField(verbose_name='Ewe(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    ram_num = models.IntegerField(verbose_name='Ram(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category10', null=True, on_delete=models.CASCADE)
    weight= models.IntegerField(verbose_name='Weight(s)')
    price = models.IntegerField(verbose_name='Price(s)')

    def __str__(self):
        return self.price

class GoatSale(models.Model):
    date = models.DateField(default=timezone.now)
    doe_num = models.IntegerField(verbose_name='Doe(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    buck_num = models.IntegerField(verbose_name='Buck(s)', null=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category11', null=True, on_delete=models.CASCADE)
    weight= models.IntegerField(verbose_name='Weight(s)')
    price = models.IntegerField(verbose_name='Price(s)')

    def __str__(self):
        return self.price

class PigSale(models.Model):
    date = models.DateField(default=timezone.now)
    sow_num = models.IntegerField(verbose_name='Sow(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    boar_num = models.IntegerField(verbose_name='Boar(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category12', null=True, on_delete=models.CASCADE)
    weight= models.IntegerField(verbose_name='Weight(s)')
    price = models.IntegerField(verbose_name='Price(s)')

    def __str__(self):
        return self.price


class GoatProcurement(models.Model):
    date = models.DateField(default=timezone.now)
    doe_num = models.IntegerField(verbose_name='Doe(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    buck_num = models.IntegerField(verbose_name='Buck(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)',null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category13', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.date
class SheepProcurement(models.Model):
    date = models.DateField(default=timezone.now)
    ewe_num = models.IntegerField(verbose_name='Ewe(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    ram_num = models.IntegerField(verbose_name='Ram(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)',null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category14', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.date

class PigProcurement(models.Model):
    date = models.DateField(default=timezone.now)
    sow_num = models.IntegerField(verbose_name='Sow(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    boar_num = models.IntegerField(verbose_name='Boar(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)',null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category15', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.date
        
class CowProcurement(models.Model):
    date = models.DateField(default=timezone.now)
    cow_num = models.IntegerField(verbose_name='Cow(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    bull_num = models.IntegerField(verbose_name='Bull(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)',null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category16', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.date 