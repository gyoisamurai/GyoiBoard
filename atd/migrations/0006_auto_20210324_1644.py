# Generated by Django 3.1.7 on 2021-03-24 07:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atd', '0005_auto_20210324_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(upload_to='atd/target/', validators=[django.core.validators.FileExtensionValidator(['h5', 'npz'])], verbose_name='Upload File'),
        ),
        migrations.AlterField(
            model_name='target',
            name='last_scan_date',
            field=models.CharField(default='N/A', max_length=255, verbose_name='Last scan date'),
        ),
        migrations.AlterField(
            model_name='target',
            name='overview',
            field=models.CharField(default='N/A', max_length=255, verbose_name='Overview'),
        ),
        migrations.AlterField(
            model_name='target',
            name='rank',
            field=models.CharField(default='N/A', max_length=1, verbose_name='Rank'),
        ),
        migrations.AlterField(
            model_name='target',
            name='status',
            field=models.CharField(default='N/A', max_length=255, verbose_name='Status'),
        ),
    ]
