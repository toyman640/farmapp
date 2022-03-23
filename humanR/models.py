from datetime import date
from email.mime import image
from django.db import models
from django.utils import timezone
from farmapp.utils import unique_slug_generatorEMP
from django.db.models.signals import pre_save
from farmrecord.validators import validate_file_size

# Create your models here.


class JobTitle(models.Model):
    title_name = models.CharField(max_length=50, verbose_name='title name')
    description = models.CharField(max_length=150, verbose_name='Description')

    def __str__(self):
        return self.title_name

class FarmSection(models.Model):
    section_name = models.CharField(max_length=50, verbose_name='Section name')
    des_type = models.CharField(max_length=150, verbose_name='Description')

    def __str__(self):
        return self.section_name

class Employee(models.Model):

    MALE = 'Male'
    FEMALE = 'Female'
    CHOOSE = ''
    SEX=[
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (CHOOSE, 'Select sex')
    ]
    date = models.DateTimeField(default=timezone.now)
    title_id = models.ForeignKey(JobTitle, verbose_name='Job title', on_delete=models.CASCADE, default=1)
    section_id = models.ForeignKey(FarmSection, verbose_name='Section',  on_delete=models.CASCADE, default=1)
    employee_SN = models.CharField(max_length=100, verbose_name='Surname')
    employee_MN = models.CharField(max_length=100, verbose_name='Middle Name')
    employee_FN= models.CharField(max_length=100, verbose_name='First Name')
    address = models.CharField(max_length=200, verbose_name='Address') 
    phone = models.IntegerField(verbose_name='Phone Number')
    sex =  models.CharField(max_length=50, choices=SEX, default=CHOOSE)
    age = models.IntegerField(verbose_name='Age', null=True)
    bank_num = models.IntegerField(verbose_name='Bank Account Number',blank=True, null=True)
    bank_name = models.CharField(max_length=100, verbose_name='Bank Name', blank=True, null=True)
    bvn = models.IntegerField(verbose_name='Bank Verification Number',blank=True, null=True)
    email = models.EmailField(max_length=150, verbose_name= 'Email Address',blank=True, null=True)
    id_type = models.CharField(max_length=50, verbose_name='ID Type',blank=True, null=True) 
    id_num = models.CharField(max_length=50, verbose_name='I.D NO.',blank=True, null=True)
    signed = models.BooleanField(default=False)
    nok_surname = models.CharField(max_length=100, verbose_name='Surname',blank=True, null=True)
    nok_oname = models.CharField(max_length=100, verbose_name='Other names',blank=True, null=True)
    nok_address = models.CharField(max_length=200, verbose_name='Address',blank=True, null=True) 
    nok_phone = models.IntegerField(verbose_name='Phone Number',blank=True, null=True)
    nok_relationship = models.CharField(max_length=50, verbose_name='Relationship With employee',blank=True, null=True) 
    guarantor = models.CharField(max_length=50, verbose_name='Guarantor Name',blank=True, null=True) 
    signed = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    image_1 = models.ImageField(verbose_name='first image', validators=[validate_file_size], blank=True, null=True, upload_to='uploads/',)
    slug = models.SlugField(max_length=150, unique=True)


    def __str__(self):
        return self.employee_SN

    def post_img(self):
        if self.image_1:
          return self.image_1.url


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generatorEMP(instance, instance.employee_SN, instance.slug)

pre_save.connect(slug_save, sender=Employee)

    
    
