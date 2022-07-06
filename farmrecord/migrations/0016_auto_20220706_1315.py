# Generated by Django 3.0.3 on 2022-07-06 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmrecord', '0015_auto_20220706_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cowcensuspop',
            name='bull_population',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Bulls Population'),
        ),
        migrations.AlterField(
            model_name='cowcensuspop',
            name='calf_population',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Calves Population'),
        ),
        migrations.AlterField(
            model_name='cowcensuspop',
            name='cow_population',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Cows Population'),
        ),
        migrations.AlterField(
            model_name='goatcensuspop',
            name='buck_population',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Bucks Population'),
        ),
        migrations.AlterField(
            model_name='goatcensuspop',
            name='doe_population',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Does Population'),
        ),
        migrations.AlterField(
            model_name='goatcensuspop',
            name='kid_population',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Kids Population'),
        ),
        migrations.AlterField(
            model_name='sheepcensuspop',
            name='ewe_population',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Ewes Population'),
        ),
        migrations.AlterField(
            model_name='sheepcensuspop',
            name='lamb_population',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Lambs Population'),
        ),
        migrations.AlterField(
            model_name='sheepcensuspop',
            name='ram_population',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Rams Population'),
        ),
    ]
