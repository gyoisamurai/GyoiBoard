# Generated by Django 3.1.7 on 2021-03-24 20:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atd', '0006_auto_20210324_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='target_path',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(upload_to='atd/target/%Y%m%d%H%M%S%f', validators=[django.core.validators.FileExtensionValidator(['h5', 'npz'])], verbose_name='Upload File'),
        ),
        migrations.AlterField(
            model_name='target',
            name='rank',
            field=models.CharField(default='N/A', max_length=10, verbose_name='Rank'),
        ),
    ]