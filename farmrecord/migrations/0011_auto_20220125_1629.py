# Generated by Django 3.0.3 on 2022-01-25 15:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('farmrecord', '0010_auto_20220125_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='CowCensusPop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'), ('', 'Select month')], max_length=50)),
                ('cat_population', models.PositiveIntegerField(verbose_name='Cattle Population')),
            ],
        ),
        migrations.CreateModel(
            name='GoatCensusPop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'), ('', 'Select month')], max_length=50)),
                ('got_population', models.PositiveIntegerField(verbose_name='Goat Population')),
            ],
        ),
        migrations.CreateModel(
            name='PigCensusPop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'), ('', 'Select month')], max_length=50)),
                ('pig_population', models.PositiveIntegerField(verbose_name='Pig Population')),
            ],
        ),
        migrations.CreateModel(
            name='SheepCensusPop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'), ('', 'Select month')], max_length=50)),
                ('shp_population', models.PositiveIntegerField(verbose_name='Sheep Population')),
            ],
        ),
        migrations.AlterField(
            model_name='cowsale',
            name='total_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Toatl Price(s)'),
        ),
        migrations.AlterField(
            model_name='goatsale',
            name='total_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total Price(s)'),
        ),
        migrations.AlterField(
            model_name='pigsale',
            name='total_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total Price(s)'),
        ),
        migrations.AlterField(
            model_name='sheepsale',
            name='total_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total Price(s)'),
        ),
    ]
