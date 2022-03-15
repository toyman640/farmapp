from django.db import models

# Create your models here.

class Employee(models.Model):

    employee_SN = models.CharField(max_length=100, verbose_name='Surname')
    employee_MN = models.CharField(max_length=100, verbose_name='Middle Name')
    employee_FN= models.CharField(max_length=100, verbose_name='First Name')
    address = models.CharField(max_length=200, verbose_name='Address')
    phone = models.IntegerField(max_length=50, verbose_name='Phone Number')
    
    
