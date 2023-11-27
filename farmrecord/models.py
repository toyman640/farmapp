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
    cow_num = models.IntegerField(verbose_name='Cow(s)', default=0)
    bull_num = models.IntegerField(verbose_name='Bull(s)', default=0)
    calves = models.IntegerField(verbose_name='calve(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category1', null=True, on_delete=models.CASCADE, default=17)
    size = models.CharField(max_length=100, verbose_name='Size(s)')
    comment = models.TextField(max_length=500, verbose_name='Cause of mortality' , blank=True)
    image_1 = models.ImageField(verbose_name='first image',validators=[validate_file_size], blank=True, null=True, upload_to='uploads/',)
    image_2 = models.ImageField(verbose_name=' second image',validators=[validate_file_size], blank=True, null=True, upload_to='uploads/')
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True)

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

    
def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.location, instance.slug)

pre_save.connect(slug_save, sender=CowMortality)


class SheepMortality(models.Model):
    mortality = models.CharField(max_length=10, verbose_name='mortality')
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200, verbose_name='loaction(s)')
    ewe_num = models.IntegerField(verbose_name='Ewe(s)', default=0)
    ram_num = models.IntegerField(verbose_name='Ram(s)', default=0)
    lamb = models.IntegerField(verbose_name='lamb(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category2', null=True, on_delete=models.CASCADE, default=19)
    size = models.CharField(max_length=100, verbose_name='Size(s)')
    comment = models.TextField(max_length=500, verbose_name='Cause of mortality' , blank=True)
    image_1 = models.ImageField(verbose_name='first image',validators=[validate_file_size], blank=True, null=True, upload_to='uploads/',)
    image_2 = models.ImageField(verbose_name=' second image',validators=[validate_file_size], blank=True, null=True, upload_to='uploads/')
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True)

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

pre_save.connect(slug_save, sender=SheepMortality)


class GoatMortality(models.Model):
    mortality = models.CharField(max_length=10, verbose_name='mortality')
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200, verbose_name='loaction(s)')
    doe_num = models.IntegerField(verbose_name='Doe(s)', default=0)
    buck_num = models.IntegerField(verbose_name='Buck(s)', default=0)
    kid = models.IntegerField(verbose_name='kid(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category3', null=True, on_delete=models.CASCADE, default=20)
    size = models.CharField(max_length=100, verbose_name='Size(s)')
    comment = models.TextField(max_length=500, verbose_name='Cause of mortality' , blank=True)
    image_1 = models.ImageField(verbose_name='first image',validators=[validate_file_size], blank=True, null=True, upload_to='uploads/',)
    image_2 = models.ImageField(verbose_name=' second image',validators=[validate_file_size], blank=True, null=True, upload_to='uploads/')
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True)

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

pre_save.connect(slug_save, sender=GoatMortality)

class PigMortality(models.Model):
    mortality = models.CharField(max_length=10, verbose_name='mortality')
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200, verbose_name='loaction(s)')
    sow_num = models.IntegerField(verbose_name='Sow(s)', default=0)
    boar_num = models.IntegerField(verbose_name='Boar(s)',default=0)
    nursing_num = models.IntegerField(verbose_name='Nursing Mother(s)', default=0)
    hogs_num = models.IntegerField(verbose_name='Hog(s)',default=0)
    growers_num = models.IntegerField(verbose_name='Grower(s)', default=0)
    weaners_num = models.IntegerField(verbose_name='Weaner(s)',default=0)
    drysows_num = models.IntegerField(verbose_name='Dry Sow(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category4', null=True, on_delete=models.CASCADE, default=18)
    size = models.CharField(max_length=100, verbose_name='Size(s)')
    comment = models.TextField(max_length=500, verbose_name='Cause of mortality' , blank=True)
    pigglet = models.IntegerField(verbose_name='Pigglet(s)', default=0)
    commentp = models.TextField(max_length=500, verbose_name='Cause of mortality' , blank=True)
    image_1 = models.ImageField(verbose_name='first image',validators=[validate_file_size], blank=True, null=True, upload_to='uploads/',)
    image_2 = models.ImageField(verbose_name=' second image',validators=[validate_file_size], blank=True, null=True, upload_to='uploads/')
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True)

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

pre_save.connect(slug_save, sender=PigMortality)


class SheepCulling(models.Model):
    date = models.DateTimeField(default=timezone.now)
    ewe_num = models.IntegerField(verbose_name='Ewe(s)', default=0)
    ram_num = models.IntegerField(verbose_name='Ram(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category5', null=True, on_delete=models.CASCADE, default=27)
    location = models.CharField(max_length=500, verbose_name='Location(s)')
    reason = models.TextField(max_length=500, verbose_name='Reason', blank=True)
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.reason   

pre_save.connect(slug_save, sender=SheepCulling)       

class CowCulling(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cow_num = models.IntegerField(verbose_name='Cow(s)', default=0)
    bull_num = models.IntegerField(verbose_name='Bull(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category6', null=True, on_delete=models.CASCADE, default=25)
    location = models.CharField(max_length=500, verbose_name='Location(s)')
    reason = models.TextField(max_length=500, verbose_name='Reason', blank=True)
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.reason

pre_save.connect(slug_save, sender=CowCulling)

class GoatCulling(models.Model):
    date = models.DateTimeField(default=timezone.now)
    doe_num = models.IntegerField(verbose_name='Doe(s)', default=0)
    buck_num = models.IntegerField(verbose_name='Buck(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category7', null=True, on_delete=models.CASCADE, default=28)
    location = models.CharField(max_length=500, verbose_name='Location(s)')
    reason = models.TextField(max_length=500, verbose_name='Reason', blank=True)
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.reason   

pre_save.connect(slug_save, sender=GoatCulling)      

class PigCulling(models.Model):
    date = models.DateTimeField(default=timezone.now)
    sow_num = models.IntegerField(verbose_name='Sow(s)', default=0)
    boar_num = models.IntegerField(verbose_name='Boar(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category8', null=True, on_delete=models.CASCADE, default=26)
    location = models.CharField(max_length=500, verbose_name='Location(s)')
    reason = models.TextField(max_length=500, verbose_name='Reason', blank=True)
    export_to_CSV = models.BooleanField(default=False)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.reason

pre_save.connect(slug_save, sender=PigCulling)

class CowSale(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cow_num = models.IntegerField(verbose_name='Cow(s)', default=0)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price = models.IntegerField(verbose_name='Price(s)', default=0)
    bull_num = models.IntegerField(verbose_name='Bull(s)', default=0)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price1 = models.IntegerField(verbose_name='Price(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category9', null=True, on_delete=models.CASCADE, default=33)
    weight= models.CharField(max_length=100,verbose_name='Weight(s)',blank=True, null=True,)
    total_price = models.IntegerField(verbose_name='Toatl Price(s)', default=0)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)

class SheepSale(models.Model):
    date = models.DateTimeField(default=timezone.now)
    ewe_num = models.IntegerField(verbose_name='Ewe(s)', default=0)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price = models.IntegerField(verbose_name='Price(s)',default=0)
    ram_num = models.IntegerField(verbose_name='Ram(s)', default=0)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price1 = models.IntegerField(verbose_name='Price(s)',default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category10', null=True, on_delete=models.CASCADE, default=35)
    weight= models.CharField(max_length=100,verbose_name='Weight(s)',blank=True, null=True,)
    total_price = models.IntegerField(verbose_name='Total Price(s)', default=0)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.total_price

class GoatSale(models.Model):
    date = models.DateTimeField(default=timezone.now)
    doe_num = models.IntegerField(verbose_name='Doe(s)',default=0)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True,)
    price = models.IntegerField(verbose_name='Price(s)',default=0)
    buck_num = models.IntegerField(verbose_name='Buck(s)',default=0)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price1 = models.IntegerField(verbose_name='Price(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category11', null=True, on_delete=models.CASCADE, default=36)
    weight= models.CharField(max_length=100,verbose_name='Weight(s)',blank=True, null=True,)
    total_price = models.IntegerField(verbose_name='Total Price(s)', default=0)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.total_price

class PigSale(models.Model):
    date = models.DateTimeField(default=timezone.now)
    sow_num = models.IntegerField(verbose_name='Sow(s)', default=0)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price = models.IntegerField(verbose_name='Price(s)', default=0)
    boar_num = models.IntegerField(verbose_name='Boar(s)', default=0)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    price1 = models.IntegerField(verbose_name='Price(s)', default=0)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category12', null=True, on_delete=models.CASCADE, default=34)
    weight= models.CharField(max_length=100,verbose_name='Weight(s)',blank=True, null=True,)
    total_price = models.IntegerField(verbose_name='Total Price(s)', default=0)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.total_price


class GoatProcurement(models.Model):
    date = models.DateTimeField(default=timezone.now)
    doe_num = models.IntegerField(verbose_name='Doe(s)', default=0)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    buck_num = models.IntegerField(verbose_name='Buck(s)', default=0)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)',blank=True,null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category13', null=True, on_delete=models.CASCADE, default=32)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.date

class SheepProcurement(models.Model):
    date = models.DateTimeField(default=timezone.now)
    ewe_num = models.IntegerField(verbose_name='Ewe(s)', default=0)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    ram_num = models.IntegerField(verbose_name='Ram(s)', default=0)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)', blank=True,null=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category14', null=True, on_delete=models.CASCADE, default=31)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.date

class PigProcurement(models.Model):
    date = models.DateTimeField(default=timezone.now)
    sow_num = models.IntegerField(verbose_name='Sow(s)',default=0)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    boar_num = models.IntegerField(verbose_name='Boar(s)', default=0)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)',null=True, blank=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category15', null=True, on_delete=models.CASCADE, default=30)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.date
        
class CowProcurement(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cow_num = models.IntegerField(verbose_name='Cow(s)', default=0)
    size = models.CharField(max_length=100, verbose_name='Size(s)', blank=True, null=True)
    bull_num = models.IntegerField(verbose_name='Bull(s)', default=0)
    size1 = models.CharField(max_length=100, verbose_name='Size(s)',null=True, blank=True)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category16', null=True, on_delete=models.CASCADE, default=29)
    export_to_CSV = models.BooleanField(default=False)

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
    date = models.DateTimeField(default=timezone.now)
    month = models.CharField(max_length=50, choices=MONTHS, default=CHOOSE)
    cow_population = models.PositiveIntegerField(verbose_name='Cows Population', null=True, blank=True, default=0)
    bull_population = models.PositiveIntegerField(verbose_name='Bulls Population', null=True, blank=True, default=0)
    calf_population = models.PositiveIntegerField(verbose_name='Calves Population', null=True, blank=True, default=0)

    def __str__(self):
        return self.month

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
    date = models.DateTimeField(default=timezone.now)
    month = models.CharField(max_length=50, choices=MONTHS, default=CHOOSE)
    doe_population = models.PositiveIntegerField(verbose_name='Does Population', null=True, blank=True, default=0)
    buck_population = models.PositiveIntegerField(verbose_name='Bucks Population', null=True, blank=True, default=0)
    kid_population = models.PositiveIntegerField(verbose_name='Kids Population', null=True, blank=True, default=0)

    def __str__(self):
        return self.month 

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
    date = models.DateTimeField(default=timezone.now)
    month = models.CharField(max_length=50, choices=MONTHS, default=CHOOSE)
    matured_pigs = models.PositiveIntegerField(verbose_name='Matured Pigs', null=True, blank=True, default=0)
    pigglets = models.PositiveIntegerField(verbose_name='Pigglets', null=True, blank=True, default=0)

    def __str__(self):
        return self.month 

    def addp(self):
        return self.matured_pigs + self.pigglets

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
    date = models.DateTimeField(default=timezone.now)
    month = models.CharField(max_length=50, choices=MONTHS, default=CHOOSE)
    ewe_population = models.PositiveIntegerField(verbose_name='Ewes Population', null=True, blank=True, default=0)
    ram_population = models.PositiveIntegerField(verbose_name='Rams Population', null=True, blank=True, default=0)
    lamb_population = models.PositiveIntegerField(verbose_name='Lambs Population', null=True, blank=True, default=0)

    def __str__(self):
        return self.month 

    def adds(self):
        return self.ewe_population + self.ram_population + self.lamb_population

class CowBirth(models.Model):
    date = models.DateTimeField(default=timezone.now)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category17', null=True, on_delete=models.CASCADE, default=22)
    clavings_num = models.IntegerField(verbose_name='Calvings Amount', default=0)
    claves_num = models.IntegerField(verbose_name='Calves Amount', default=0)
    still_birthc = models.IntegerField(verbose_name='Stillbirth', default=0)
    weak_claves = models.IntegerField(verbose_name='Weak Calf/ves', default=0)
    defected_calf = models.IntegerField(verbose_name='Defected Claf/ves', default=0)
    comment_c  = models.TextField(max_length=500, verbose_name='Comment' , blank=True)

    def __str__(self):
        return str(self.calvings_num)


class SheepBirth(models.Model):
    date = models.DateTimeField(default=timezone.now)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category18', null=True, on_delete=models.CASCADE, default=23)
    lambings_num = models.IntegerField(verbose_name='Lambings Amount', default=0)
    lambs_num = models.IntegerField(verbose_name='Lambs Amount', default=0)
    still_births = models.IntegerField(verbose_name='Stillbirth ', default=0)
    weak_lamb = models.IntegerField(verbose_name='Weak Lamb(s)', default=0)
    defected_lamb = models.IntegerField(verbose_name='Defected Lamb(s)', default=0)
    comment_s = models.TextField(max_length=500, verbose_name='Comment' , blank=True)


    def __str__(self):
        return str(self.lambings_num)


class GoatBirth(models.Model):
    date = models.DateTimeField(default=timezone.now)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category19', null=True, on_delete=models.CASCADE, default=24)
    kiddings_num = models.IntegerField(verbose_name='Kidding Amount', default=0)
    kids_num = models.IntegerField(verbose_name='Kids Amount', default=0)
    still_birthg = models.IntegerField(verbose_name='Stillbirth ', default=0)
    weak_kid = models.IntegerField(verbose_name='Weak Kid(s)', default=0)
    defected_kid = models.IntegerField(verbose_name='Defected Kid(s)', default=0)
    comment_g = models.TextField(max_length=500, verbose_name='Comment' , blank=True)

    def __str__(self):
        return str(self.kiddings_num)


class PigBirth(models.Model):
    date = models.DateTimeField(default=timezone.now)
    section = models.ForeignKey(Section, verbose_name='Section', related_name='category20', null=True, on_delete=models.CASCADE, default=21)
    farrowing_num = models.IntegerField(verbose_name='Farrowing Amount', default=0)
    pigglets_num = models.IntegerField(verbose_name='Pigglets Amount', default=0)
    still_birthp = models.IntegerField(verbose_name='Stillbirth ', default=0)
    weak_pigglet = models.IntegerField(verbose_name='Weak Pigglet(s)', default=0)
    defected_pigglet = models.IntegerField(verbose_name='Defected Pigglet(s)', default=0)
    devoured_pigglet = models.IntegerField(verbose_name='Devoured Pigglet(s)', default=0)
    overlaying = models.IntegerField(verbose_name='Overlaying', default=0)
    comment_p = models.TextField(max_length=500, verbose_name='Comment' , blank=True)


    def __str__(self):
        return str(self.farrowing_num)
    



