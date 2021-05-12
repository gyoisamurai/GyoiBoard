# Generated by Django 3.1.7 on 2021-05-12 12:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gyoithon', '0020_auto_20210512_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='scan_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 56, 57, 264931, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='domain',
            name='name_server',
            field=models.TextField(default='N/A', max_length=1000, verbose_name='Name Server'),
        ),
        migrations.AlterField(
            model_name='domain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 56, 57, 263693, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 56, 57, 263090, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 56, 57, 264432, tzinfo=utc)),
        ),
    ]
