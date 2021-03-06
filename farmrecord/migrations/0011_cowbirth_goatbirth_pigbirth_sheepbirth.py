# Generated by Django 3.0.3 on 2022-06-27 12:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('farmrecord', '0010_auto_20220623_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='SheepBirth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('lambings_num', models.IntegerField(default=0, verbose_name='Lambings Amount')),
                ('lambs_num', models.IntegerField(default=0, verbose_name='Lambs Amount')),
                ('still_births', models.IntegerField(default=0, verbose_name='Stillbirth ')),
                ('weak_lamb', models.IntegerField(default=0, verbose_name='Weak Lamb(s)')),
                ('defected_lamb', models.IntegerField(default=0, verbose_name='Defected Lamb(s)')),
                ('comment_s', models.TextField(blank=True, max_length=500, verbose_name='Comment')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category18', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='PigBirth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('farrowing_num', models.IntegerField(default=0, verbose_name='Farrowing Amount')),
                ('pigglets_num', models.IntegerField(default=0, verbose_name='Pigglets Amount')),
                ('still_birthp', models.IntegerField(default=0, verbose_name='Stillbirth ')),
                ('weak_pigglet', models.IntegerField(default=0, verbose_name='Weak Pigglet(s)')),
                ('defected_pigglet', models.IntegerField(default=0, verbose_name='Defected Pigglet(s)')),
                ('devoured_pigglet', models.IntegerField(default=0, verbose_name='Devoured Pigglet(s)')),
                ('overlaying', models.IntegerField(default=0, verbose_name='Overlaying')),
                ('comment_p', models.TextField(blank=True, max_length=500, verbose_name='Comment')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category20', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='GoatBirth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('kiddings_num', models.IntegerField(default=0, verbose_name='Kiddings Amount')),
                ('kids_num', models.IntegerField(default=0, verbose_name='Kids Amount')),
                ('still_birthg', models.IntegerField(default=0, verbose_name='Stillbirth ')),
                ('weak_kid', models.IntegerField(default=0, verbose_name='Weak Kid(s)')),
                ('defected_lamb', models.IntegerField(default=0, verbose_name='Defected Kid(s)')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category19', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
        migrations.CreateModel(
            name='CowBirth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('clavings_num', models.IntegerField(default=0, verbose_name='Calvings Amount')),
                ('claves_num', models.IntegerField(default=0, verbose_name='Calves Amount')),
                ('still_birthc', models.IntegerField(default=0, verbose_name='Stillbirth')),
                ('weak_claves', models.IntegerField(default=0, verbose_name='Weak Calf/ves')),
                ('defected_calf', models.IntegerField(default=0, verbose_name='Defected Claf/ves')),
                ('comment_c', models.TextField(blank=True, max_length=500, verbose_name='Comment')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category17', to='farmrecord.Section', verbose_name='Section')),
            ],
        ),
    ]
