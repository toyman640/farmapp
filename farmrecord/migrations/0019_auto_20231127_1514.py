# Generated by Django 3.0.3 on 2023-11-27 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farmrecord', '0018_auto_20231127_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cowbirth',
            name='section',
            field=models.ForeignKey(default=22, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category17', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='cowculling',
            name='section',
            field=models.ForeignKey(default=25, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category6', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='cowmortality',
            name='section',
            field=models.ForeignKey(default=17, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category1', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='cowprocurement',
            name='section',
            field=models.ForeignKey(default=29, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category16', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='cowsale',
            name='section',
            field=models.ForeignKey(default=33, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category9', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='goatbirth',
            name='section',
            field=models.ForeignKey(default=24, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category19', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='goatculling',
            name='section',
            field=models.ForeignKey(default=28, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category7', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='goatmortality',
            name='section',
            field=models.ForeignKey(default=20, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category3', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='goatprocurement',
            name='section',
            field=models.ForeignKey(default=32, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category13', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='goatsale',
            name='section',
            field=models.ForeignKey(default=36, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category11', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='pigbirth',
            name='section',
            field=models.ForeignKey(default=21, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category20', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='pigculling',
            name='section',
            field=models.ForeignKey(default=26, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category8', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='pigmortality',
            name='section',
            field=models.ForeignKey(default=18, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category4', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='pigprocurement',
            name='section',
            field=models.ForeignKey(default=30, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category15', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='pigsale',
            name='section',
            field=models.ForeignKey(default=34, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category12', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='sheepbirth',
            name='section',
            field=models.ForeignKey(default=23, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category18', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='sheepculling',
            name='section',
            field=models.ForeignKey(default=27, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category5', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='sheepmortality',
            name='section',
            field=models.ForeignKey(default=19, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category2', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='sheepprocurement',
            name='section',
            field=models.ForeignKey(default=31, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category14', to='farmrecord.Section', verbose_name='Section'),
        ),
        migrations.AlterField(
            model_name='sheepsale',
            name='section',
            field=models.ForeignKey(default=35, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category10', to='farmrecord.Section', verbose_name='Section'),
        ),
    ]