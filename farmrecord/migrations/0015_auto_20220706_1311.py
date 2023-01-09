# Generated by Django 3.0.3 on 2022-07-06 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmrecord', '0014_auto_20220701_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pigcensuspop',
            name='matured_pigs',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Matured Pigs'),
        ),
        migrations.AlterField(
            model_name='pigcensuspop',
            name='pigglets',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Pigglets'),
        ),
    ]