# Generated by Django 3.1.7 on 2021-03-24 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atd', '0004_auto_20210324_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file',
            field=models.FileField(upload_to='atd/target/%Y%m%d%H%M%S%f'),
        ),
        migrations.AlterField(
            model_name='target',
            name='last_scan_date',
            field=models.CharField(max_length=255, verbose_name='Last scan date'),
        ),
    ]
