# Generated by Django 3.1.7 on 2021-05-11 09:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gyoithon', '0013_auto_20210510_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 9, 7, 57, 538054, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 9, 7, 57, 537477, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 11, 9, 7, 57, 538664, tzinfo=utc)),
        ),
    ]
