# Generated by Django 3.0.3 on 2022-01-08 13:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('farmrecord', '0007_auto_20211222_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cowmortality',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cowsale',
            name='bull_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='Bull(s)'),
        ),
        migrations.AlterField(
            model_name='pigprocurement',
            name='size1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)'),
        ),
        migrations.AlterField(
            model_name='pigsale',
            name='boar_num',
            field=models.IntegerField(blank=True, null=True, verbose_name='Boar(s)'),
        ),
    ]
