# Generated by Django 3.0.3 on 2022-07-26 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='export_to_CSV',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchases',
            name='i_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Price per Quantity'),
        ),
        migrations.AlterField(
            model_name='purchases',
            name='price',
            field=models.IntegerField(verbose_name='Total Price'),
        ),
    ]
