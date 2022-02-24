# Generated by Django 3.0.3 on 2022-02-24 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CowCensusPop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'), ('', 'Select month')], default='', max_length=50)),
                ('cow_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cows Population')),
                ('bull_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Bulls Population')),
                ('calf_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Calves Population')),
            ],
        ),
        migrations.CreateModel(
            name='GoatCensusPop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'), ('', 'Select month')], default='', max_length=50)),
                ('doe_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Does Population')),
                ('buck_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Bucks Population')),
                ('kid_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Kids Population')),
            ],
        ),
        migrations.CreateModel(
            name='PigCensusPop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'), ('', 'Select month')], default='', max_length=50)),
                ('sow_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Sow Population')),
                ('boar_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Boar Population')),
                ('hog_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Hogs Population')),
                ('weaner_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Weaners Population')),
                ('grower_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Growers Population')),
                ('dry_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Dry Sows Population')),
            ],
        ),
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
            name='SheepCensusPop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December'), ('', 'Select month')], default='', max_length=50)),
                ('ewe_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Ewes Population')),
                ('ram_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Rams Population')),
                ('lamb_population', models.PositiveIntegerField(blank=True, null=True, verbose_name='Lambs Population')),
            ],
        ),
        migrations.CreateModel(
            name='Userp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_boss', models.BooleanField(default=False, verbose_name='Is boss')),
                ('is_hr', models.BooleanField(default=False, verbose_name='Is hr')),
                ('is_supervisor', models.BooleanField(default=False, verbose_name='Is supervisor')),
                ('is_account', models.BooleanField(default=False, verbose_name='Is account')),
                ('is_maintenance', models.BooleanField(default=False, verbose_name='Is maintenance')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SheepSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ewe_num', models.IntegerField(default=0, verbose_name='Ewe(s)')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('price', models.IntegerField(default=0, verbose_name='Price(s)')),
                ('ram_num', models.IntegerField(default=0, verbose_name='Ram(s)')),
                ('size1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('price1', models.IntegerField(default=0, verbose_name='Price(s)')),
                ('weight', models.CharField(blank=True, max_length=100, null=True, verbose_name='Weight(s)')),
                ('total_price', models.IntegerField(default=0, verbose_name='Total Price(s)')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category10', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='SheepProcurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ewe_num', models.IntegerField(default=0, verbose_name='Ewe(s)')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('ram_num', models.IntegerField(default=0, verbose_name='Ram(s)')),
                ('size1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category14', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='SheepMortality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mortality', models.CharField(max_length=10, verbose_name='mortality')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=200, verbose_name='loaction(s)')),
                ('ewe_num', models.IntegerField(default=0, verbose_name='Ewe(s)')),
                ('ram_num', models.IntegerField(default=0, verbose_name='Ram(s)')),
                ('lamb', models.IntegerField(default=0, verbose_name='lamb(s)')),
                ('size', models.CharField(max_length=100, verbose_name='Size(s)')),
                ('comment', models.TextField(blank=True, max_length=500, verbose_name='Cause of mortality')),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='first image')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name=' second image')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category2', to='farmrecord.Section', verbose_name='Section')),
            ],
            options={
                'verbose_name_plural': 'Sheep mortality',
            },
        ),
        migrations.CreateModel(
            name='SheepCulling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ewe_num', models.IntegerField(default=0, verbose_name='Ewe(s)')),
                ('ram_num', models.IntegerField(default=0, verbose_name='Ram(s)')),
                ('location', models.CharField(max_length=500, verbose_name='Location(s)')),
                ('reason', models.TextField(blank=True, max_length=500, verbose_name='Reason')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category5', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='PigSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('sow_num', models.IntegerField(default=0, verbose_name='Sow(s)')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('price', models.IntegerField(default=0, verbose_name='Price(s)')),
                ('boar_num', models.IntegerField(default=0, verbose_name='Boar(s)')),
                ('size1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('price1', models.IntegerField(default=0, verbose_name='Price(s)')),
                ('weight', models.CharField(blank=True, max_length=100, null=True, verbose_name='Weight(s)')),
                ('total_price', models.IntegerField(default=0, verbose_name='Total Price(s)')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category12', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='PigProcurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('sow_num', models.IntegerField(default=0, verbose_name='Sow(s)')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('boar_num', models.IntegerField(default=0, verbose_name='Boar(s)')),
                ('size1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category15', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='PigMortality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mortality', models.CharField(max_length=10, verbose_name='mortality')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=200, verbose_name='loaction(s)')),
                ('sow_num', models.IntegerField(default=0, verbose_name='Sow(s)')),
                ('boar_num', models.IntegerField(default=0, verbose_name='Boar(s)')),
                ('pigglet', models.IntegerField(default=0, verbose_name='Pigglet(s)')),
                ('size', models.CharField(max_length=100, verbose_name='Size(s)')),
                ('comment', models.TextField(blank=True, max_length=500, verbose_name='Cause of mortality')),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='first image')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name=' second image')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category4', to='farmrecord.Section', verbose_name='Section')),
            ],
            options={
                'verbose_name_plural': 'Pig mortality',
            },
        ),
        migrations.CreateModel(
            name='PigCulling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('sow_num', models.IntegerField(default=0, verbose_name='Sow(s)')),
                ('boar_num', models.IntegerField(default=0, verbose_name='Boar(s)')),
                ('location', models.CharField(max_length=500, verbose_name='Location(s)')),
                ('reason', models.TextField(blank=True, max_length=500, verbose_name='Reason')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category8', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='GoatSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('doe_num', models.IntegerField(default=0, verbose_name='Doe(s)')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('price', models.IntegerField(default=0, verbose_name='Price(s)')),
                ('buck_num', models.IntegerField(default=0, verbose_name='Buck(s)')),
                ('size1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('price1', models.IntegerField(default=0, verbose_name='Price(s)')),
                ('weight', models.CharField(blank=True, max_length=100, null=True, verbose_name='Weight(s)')),
                ('total_price', models.IntegerField(default=0, verbose_name='Total Price(s)')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category11', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='GoatProcurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('doe_num', models.IntegerField(default=0, verbose_name='Doe(s)')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('buck_num', models.IntegerField(default=0, verbose_name='Buck(s)')),
                ('size1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category13', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='GoatMortality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mortality', models.CharField(max_length=10, verbose_name='mortality')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=200, verbose_name='loaction(s)')),
                ('doe_num', models.IntegerField(default=0, verbose_name='Doe(s)')),
                ('buck_num', models.IntegerField(default=0, verbose_name='Buck(s)')),
                ('kid', models.IntegerField(default=0, verbose_name='kid(s)')),
                ('size', models.CharField(max_length=100, verbose_name='Size(s)')),
                ('comment', models.TextField(blank=True, max_length=500, verbose_name='Cause of mortality')),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='first image')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name=' second image')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category3', to='farmrecord.Section', verbose_name='Section')),
            ],
            options={
                'verbose_name_plural': 'Goat mortality',
            },
        ),
        migrations.CreateModel(
            name='GoatCulling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('doe_num', models.IntegerField(default=0, verbose_name='Doe(s)')),
                ('buck_num', models.IntegerField(default=0, verbose_name='Buck(s)')),
                ('location', models.CharField(max_length=500, verbose_name='Location(s)')),
                ('reason', models.TextField(blank=True, max_length=500, verbose_name='Reason')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category7', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='CowSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('cow_num', models.IntegerField(default=0, verbose_name='Cow(s)')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('price', models.IntegerField(default=0, verbose_name='Price(s)')),
                ('bull_num', models.IntegerField(default=0, verbose_name='Bull(s)')),
                ('size1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('price1', models.IntegerField(default=0, verbose_name='Price(s)')),
                ('weight', models.CharField(blank=True, max_length=100, null=True, verbose_name='Weight(s)')),
                ('total_price', models.IntegerField(default=0, verbose_name='Toatl Price(s)')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category9', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='CowProcurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('cow_num', models.IntegerField(default=0, verbose_name='Cow(s)')),
                ('size', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('bull_num', models.IntegerField(default=0, verbose_name='Bull(s)')),
                ('size1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Size(s)')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category16', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='CowMortality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mortality', models.CharField(max_length=10, verbose_name='mortality')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=200, verbose_name='loaction(s)')),
                ('cow_num', models.IntegerField(default=0, verbose_name='Cow(s)')),
                ('bull_num', models.IntegerField(default=0, verbose_name='Bull(s)')),
                ('calves', models.IntegerField(default=0, verbose_name='calve(s)')),
                ('size', models.CharField(max_length=100, verbose_name='Size(s)')),
                ('comment', models.TextField(blank=True, max_length=500, verbose_name='Cause of mortality')),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='first image')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name=' second image')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category1', to='farmrecord.Section', verbose_name='Section')),
            ],
            options={
                'verbose_name_plural': 'Cow mortality',
            },
        ),
        migrations.CreateModel(
            name='CowCulling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('cow_num', models.IntegerField(default=0, verbose_name='Cow(s)')),
                ('bull_num', models.IntegerField(default=0, verbose_name='Bull(s)')),
                ('location', models.CharField(max_length=500, verbose_name='Location(s)')),
                ('reason', models.TextField(blank=True, max_length=500, verbose_name='Reason')),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category6', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
    ]
