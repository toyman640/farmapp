# Generated by Django 3.0.3 on 2022-03-31 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humanR', '0008_employee_job_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='job_desc',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Job Description'),
        ),
    ]