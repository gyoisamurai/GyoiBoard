# Generated by Django 3.1.7 on 2021-05-12 12:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gyoithon', '0018_auto_20210512_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='scan_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 47, 1, 862206, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='domain',
            name='rank',
            field=models.IntegerField(choices=[(0, '-----'), (1, 'Secure'), (2, 'Normal'), (3, 'Weak'), (4, 'Critical')], default=0, verbose_name='Rank'),
        ),
        migrations.AlterField(
            model_name='domain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 47, 1, 860969, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='rank',
            field=models.IntegerField(choices=[(0, '-----'), (1, 'Secure'), (2, 'Normal'), (3, 'Weak'), (4, 'Critical')], default=0, verbose_name='Rank'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 47, 1, 860342, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='cloud_type',
            field=models.IntegerField(choices=[(0, '-----'), (1, 'Amazon Web Service'), (2, 'Google Cloud Platform'), (3, 'Microsoft Azure')], default=0, verbose_name='Cloud Type'),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='rank',
            field=models.IntegerField(choices=[(0, '-----'), (1, 'Secure'), (2, 'Normal'), (3, 'Weak'), (4, 'Critical')], default=0, verbose_name='Rank'),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 12, 47, 1, 861719, tzinfo=utc)),
        ),
    ]