# Generated by Django 3.1.7 on 2021-05-12 12:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gyoithon', '0021_auto_20210512_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='scan_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 58, 30, 478736, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='domain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 58, 30, 477142, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='overview',
            field=models.TextField(default='', max_length=1000, verbose_name='Overview'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 58, 30, 476290, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 58, 30, 478179, tzinfo=utc)),
        ),
    ]
