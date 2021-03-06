# Generated by Django 3.0.3 on 2022-02-28 13:13

from django.db import migrations, models
import farmrecord.validators


class Migration(migrations.Migration):

    dependencies = [
        ('farmrecord', '0002_auto_20220228_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cowmortality',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/', validators=[farmrecord.validators.validate_file_size], verbose_name=' second image'),
        ),
        migrations.AlterField(
            model_name='goatmortality',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/', validators=[farmrecord.validators.validate_file_size], verbose_name='first image'),
        ),
        migrations.AlterField(
            model_name='goatmortality',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/', validators=[farmrecord.validators.validate_file_size], verbose_name=' second image'),
        ),
        migrations.AlterField(
            model_name='pigmortality',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/', validators=[farmrecord.validators.validate_file_size], verbose_name='first image'),
        ),
        migrations.AlterField(
            model_name='pigmortality',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/', validators=[farmrecord.validators.validate_file_size], verbose_name=' second image'),
        ),
        migrations.AlterField(
            model_name='sheepmortality',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/', validators=[farmrecord.validators.validate_file_size], verbose_name='first image'),
        ),
        migrations.AlterField(
            model_name='sheepmortality',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/', validators=[farmrecord.validators.validate_file_size], verbose_name=' second image'),
        ),
    ]
