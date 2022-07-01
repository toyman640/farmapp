# Generated by Django 3.0.3 on 2022-07-01 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmrecord', '0012_auto_20220627_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='pigcensuspop',
            name='matured_pigs',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Matured Pigs'),
        ),
        migrations.AddField(
            model_name='pigcensuspop',
            name='pigglets',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Pigglets'),
        ),
        migrations.AlterField(
            model_name='goatbirth',
            name='kiddings_num',
            field=models.IntegerField(default=0, verbose_name='Kidding Amount'),
        ),
    ]
