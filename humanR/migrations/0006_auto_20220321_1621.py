# Generated by Django 3.0.3 on 2022-03-21 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humanR', '0005_auto_20220321_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=50, verbose_name='Section name')),
                ('des_type', models.CharField(max_length=150, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_name', models.CharField(max_length=50, verbose_name='title name')),
                ('description', models.CharField(max_length=150, verbose_name='Description')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='section_id',
            field=models.ManyToManyField(to='humanR.FarmSection', verbose_name='Section'),
        ),
        migrations.AddField(
            model_name='employee',
            name='title_id',
            field=models.ManyToManyField(to='humanR.JobTitle', verbose_name='Job title'),
        ),
    ]
