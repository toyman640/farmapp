# Generated by Django 3.0.3 on 2025-02-01 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmrecord', '0002_alter_animals_animal_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventtype',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='eventtype',
            name='designation',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='eventtype',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userp',
            name='is_drug',
            field=models.BooleanField(default=False, verbose_name='Is drug'),
        ),
    ]
