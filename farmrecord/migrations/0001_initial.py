# Generated by Django 3.0.3 on 2021-12-20 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sec_name', models.CharField(max_length=100, verbose_name='Section Name')),
                ('sec_desc', models.TextField(blank=True, verbose_name='Description')),
            ],
            options={
                'verbose_name_plural': 'Section',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='First name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last name')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CowMortality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mortality', models.CharField(max_length=10, verbose_name='mortality')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('loaction', models.CharField(max_length=200, verbose_name='loaction(s)')),
                ('cow_num', models.IntegerField(blank=True, verbose_name='Cow(s)')),
                ('bull_num', models.IntegerField(blank=True, verbose_name='Bull(s)')),
                ('calves', models.IntegerField(blank=True, verbose_name='calve(s)')),
                ('size', models.CharField(max_length=100, verbose_name='Size(s)')),
                ('comment', models.TextField(max_length=500, verbose_name='comment')),
                ('image_1', models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name='first image')),
                ('image_2', models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name=' second image')),
                ('section', models.ManyToManyField(to='farmrecord.Section', verbose_name='Section')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
