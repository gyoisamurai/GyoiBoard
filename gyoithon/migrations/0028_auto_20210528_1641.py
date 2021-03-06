# Generated by Django 3.1.7 on 2021-05-28 07:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gyoithon', '0027_auto_20210514_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='scan_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 28, 7, 41, 15, 320713, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='domain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 28, 7, 41, 15, 319361, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 28, 7, 41, 15, 318716, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 28, 7, 41, 15, 320172, tzinfo=utc)),
        ),
    ]
