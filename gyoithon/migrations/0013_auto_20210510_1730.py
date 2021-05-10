# Generated by Django 3.1.7 on 2021-05-10 08:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gyoithon', '0012_auto_20210510_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 8, 30, 35, 615583, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 8, 30, 35, 614995, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 8, 30, 35, 616184, tzinfo=utc)),
        ),
    ]
