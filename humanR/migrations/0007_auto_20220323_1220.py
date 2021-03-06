# Generated by Django 3.0.3 on 2022-03-23 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humanR', '0006_auto_20220321_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='section_id',
        ),
        migrations.AddField(
            model_name='employee',
            name='section_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='humanR.FarmSection', verbose_name='Section'),
        ),
        migrations.RemoveField(
            model_name='employee',
            name='title_id',
        ),
        migrations.AddField(
            model_name='employee',
            name='title_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='humanR.JobTitle', verbose_name='Job title'),
        ),
    ]
