from django.db import models
from django.utils import timezone

# Create your models here.

class PurchaseSection(models.Model):
    psec_name = models.CharField(max_length=50, verbose_name='Purchse name')
    psec_desc = models.TextField(max_length=500, verbose_name='Description', blank=True, null=True)

    def __str__(self):
        return self.psec_name


class Purchases(models.Model):
    date = models.DateTimeField(default=timezone.now)
    section = models.ForeignKey(PurchaseSection, verbose_name='Section', on_delete=models.CASCADE)
    item = models.CharField(max_length=100, verbose_name='Item')
    quantity = models.CharField(max_length=50, verbose_name='Quantity/Amount')
    i_price = models.IntegerField(verbose_name='Price per Quantity', blank=True, null=True)
    price = models.IntegerField(verbose_name='Total Price')
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.item
    