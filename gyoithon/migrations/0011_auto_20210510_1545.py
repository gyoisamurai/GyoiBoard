# Generated by Django 3.1.7 on 2021-05-10 06:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gyoithon', '0010_auto_20210510_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subdomain',
            name='related_domain',
        ),
        migrations.AddField(
            model_name='subdomain',
            name='related_domain_id',
            field=models.IntegerField(default=0, verbose_name='Related Domain ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subdomain',
            name='related_organization_id',
            field=models.IntegerField(default=0, verbose_name='Related Organization ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='domain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 6, 45, 9, 58817, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 6, 45, 9, 58181, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 10, 6, 45, 9, 59618, tzinfo=utc)),
        ),
    ]
