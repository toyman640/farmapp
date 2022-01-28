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
    date = models.DateTimeField(default=timezone.now)
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
    price = models.IntegerField(verbose_name='Price(s)', blank=True, null=True)
    bull_num = models.IntegerField(verbose_name='Bull(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price1 = models.IntegerField(verbose_name='Price(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category9', null=True, on_delete=models.CASCADE)
    weight= models.IntegerField(verbose_name='Weight(s)')
    total_price = models.IntegerField(verbose_name='Toatl Price(s)', blank=True, null=True)

    def __str__(self):
        return str(self.total_price)

class SheepSale(models.Model):
    date = models.DateField(default=timezone.now)
    ewe_num = models.IntegerField(verbose_name='Ewe(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price = models.IntegerField(verbose_name='Price(s)', blank=True, null=True)
    ram_num = models.IntegerField(verbose_name='Ram(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price1 = models.IntegerField(verbose_name='Price(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category10', null=True, on_delete=models.CASCADE)
    weight= models.IntegerField(verbose_name='Weight(s)')
    total_price = models.IntegerField(verbose_name='Total Price(s)', blank=True, null=True)

    def __str__(self):
        return self.total_price

class GoatSale(models.Model):
    date = models.DateField(default=timezone.now)
    doe_num = models.IntegerField(verbose_name='Doe(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price = models.IntegerField(verbose_name='Price(s)', null=True, blank=True)
    buck_num = models.IntegerField(verbose_name='Buck(s)', null=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price1 = models.IntegerField(verbose_name='Price(s)', null=True, blank=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category11', null=True, on_delete=models.CASCADE)
    weight= models.IntegerField(verbose_name='Weight(s)')
    total_price = models.IntegerField(verbose_name='Total Price(s)', null=True, blank=True)

    def __str__(self):
        return self.total_price

class PigSale(models.Model):
    date = models.DateField(default=timezone.now)
    sow_num = models.IntegerField(verbose_name='Sow(s)', null=True, blank=True)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price = models.IntegerField(verbose_name='Price(s)', blank=True, null=True)
    boar_num = models.IntegerField(verbose_name='Boar(s)', null=True, blank=True)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price1 = models.IntegerField(verbose_name='Price(s)', blank=True, null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category12', null=True, on_delete=models.CASCADE)
    weight= models.IntegerField(verbose_name='Weight(s)')
    total_price = models.IntegerField(verbose_name='Total Price(s)', blank=True, null=True)

    def __str__(self):
        return self.total_price


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
    size1 = models.CharField(max_length=100, verbose_name='Size(s)',null=True, blank=True)
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

class CowCensusPop(models.Model):
    JANUARY = 'January'
    FEBRUARY = 'February'
    MARCH = 'March'
    APRIL = 'April'
    MAY = 'May'
    JUNE = 'June'
    JULY = 'July'
    AUGUST = 'August'
    SEPTEMBER = 'September'
    OCTOBER = 'October'
    NOVEMBER = 'November'
    DECEMBER = 'December'
    CHOOSE = ''
    MONTHS=[
        (JANUARY, 'January'),
        (FEBRUARY, 'February'),
        (MARCH, 'March'),
        (APRIL, 'April'),
        (MAY, 'May'),
        (JUNE, 'June'),
        (JULY, 'July'),
        (AUGUST, 'August'),
        (SEPTEMBER, 'September'),
        (OCTOBER, 'October'),
        (NOVEMBER, 'November'),
        (DECEMBER, 'December'),
        (CHOOSE, 'Select month')
    ]
    date = models.DateField(default=timezone.now)
    month = models.CharField(max_length=50, choices=MONTHS, default=CHOOSE)
    cow_population = models.PositiveIntegerField(verbose_name='Cows Population', null=True, blank=True)
    bull_population = models.PositiveIntegerField(verbose_name='Bulls Population', null=True, blank=True)
    calf_population = models.PositiveIntegerField(verbose_name='Calves Population', null=True, blank=True)

    def __str__(self):
        return self.month , self.cow_population , self.calf_population, self.bull_population

    def addc(self):
        return self.cow_population + self.calf_population + self.bull_population


class GoatCensusPop(models.Model):
    JANUARY = 'January'
    FEBRUARY = 'February'
    MARCH = 'March'
    APRIL = 'April'
    MAY = 'May'
    JUNE = 'June'
    JULY = 'July'
    AUGUST = 'August'
    SEPTEMBER = 'September'
    OCTOBER = 'October'
    NOVEMBER = 'November'
    DECEMBER = 'December'
    CHOOSE = ''
    MONTHS=[
        (JANUARY, 'January'),
        (FEBRUARY, 'February'),
        (MARCH, 'March'),
        (APRIL, 'April'),
        (MAY, 'May'),
        (JUNE, 'June'),
        (JULY, 'July'),
        (AUGUST, 'August'),
        (SEPTEMBER, 'September'),
        (OCTOBER, 'October'),
        (NOVEMBER, 'November'),
        (DECEMBER, 'December'),
        (CHOOSE, 'Select month')
    ]
    date = models.DateField(default=timezone.now)
    month = models.CharField(max_length=50, choices=MONTHS, default=CHOOSE)
    doe_population = models.PositiveIntegerField(verbose_name='Does Population', null=True, blank=True)
    buck_population = models.PositiveIntegerField(verbose_name='Bucks Population', null=True, blank=True)
    kid_population = models.PositiveIntegerField(verbose_name='Kids Population', null=True, blank=True)

    def __str__(self):
        return self.month , self.doe_population , self.kid_population, self.buck_population

    def addg(self):
        return self.doe_population + self.kid_population + self.buck_population

class PigCensusPop(models.Model):
    JANUARY = 'January'
    FEBRUARY = 'February'
    MARCH = 'March'
    APRIL = 'April'
    MAY = 'May'
    JUNE = 'June'
    JULY = 'July'
    AUGUST = 'August'
    SEPTEMBER = 'September'
    OCTOBER = 'October'
    NOVEMBER = 'November'
    DECEMBER = 'December'
    CHOOSE = ''
    MONTHS=[
        (JANUARY, 'January'),
        (FEBRUARY, 'February'),
        (MARCH, 'March'),
        (APRIL, 'April'),
        (MAY, 'May'),
        (JUNE, 'June'),
        (JULY, 'July'),
        (AUGUST, 'August'),
        (SEPTEMBER, 'September'),
        (OCTOBER, 'October'),
        (NOVEMBER, 'November'),
        (DECEMBER, 'December'),
        (CHOOSE, 'Select month')
    ]
    date = models.DateField(default=timezone.now)
    month = models.CharField(max_length=50, choices=MONTHS, default=CHOOSE)
    sow_population = models.PositiveIntegerField(verbose_name='Sow Population', null=True, blank=True)
    boar_population = models.PositiveIntegerField(verbose_name='Boar Population', null=True, blank=True)
    hog_population = models.PositiveIntegerField(verbose_name='Hogs Population', null=True, blank=True)
    weaner_population = models.PositiveIntegerField(verbose_name='Weaners Population', null=True, blank=True)
    grower_population = models.PositiveIntegerField(verbose_name='Growers Population', null=True, blank=True)
    dry_population = models.PositiveIntegerField(verbose_name='Dry Sows Population', null=True, blank=True)

    def __str__(self):
        return self.month , self.sow_population , self.boar_population, self.hog_population, self.weaner_population, self.grower_population, self.dry_population

    def addp(self):
        return self.sow_population + self.boar_population + self.hog_population + self.weaner_population + self.grower_population + self.dry_population

class SheepCensusPop(models.Model):
    JANUARY = 'January'
    FEBRUARY = 'February'
    MARCH = 'March'
    APRIL = 'April'
    MAY = 'May'
    JUNE = 'June'
    JULY = 'July'
    AUGUST = 'August'
    SEPTEMBER = 'September'
    OCTOBER = 'October'
    NOVEMBER = 'November'
    DECEMBER = 'December'
    CHOOSE = ''
    MONTHS=[
        (JANUARY, 'January'),
        (FEBRUARY, 'February'),
        (MARCH, 'March'),
        (APRIL, 'April'),
        (MAY, 'May'),
        (JUNE, 'June'),
        (JULY, 'July'),
        (AUGUST, 'August'),
        (SEPTEMBER, 'September'),
        (OCTOBER, 'October'),
        (NOVEMBER, 'November'),
        (DECEMBER, 'December'),
        (CHOOSE, 'Select month')
    ]
    date = models.DateField(default=timezone.now)
    month = models.CharField(max_length=50, choices=MONTHS, default=CHOOSE)
    ewe_population = models.PositiveIntegerField(verbose_name='Ewes Population', null=True, blank=True)
    ram_population = models.PositiveIntegerField(verbose_name='Rams Population', null=True, blank=True)
    lamb_population = models.PositiveIntegerField(verbose_name='Lambs Population', null=True, blank=True)

    def __str__(self):
        return self.month , self.ewe_population , self.ram_population, self.lamb_population

    def adds(self):
        return self.ewe_population + self.ram_population + self.lamb_population