# Generated by Django 3.1.7 on 2021-05-12 08:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gyoithon', '0016_auto_20210512_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_organization_id', models.IntegerField(verbose_name='Related Organization ID')),
                ('related_domain_id', models.IntegerField(verbose_name='Related Domain ID')),
                ('related_subdomain_id', models.IntegerField(verbose_name='Related Subdomain ID')),
                ('scan_date', models.DateTimeField(default=datetime.datetime(2021, 5, 12, 8, 17, 35, 692448, tzinfo=utc))),
                ('target_port', models.IntegerField(default=80, verbose_name='Port')),
                ('assessment_url', models.CharField(default='N/A', max_length=255, verbose_name='Assessment URL')),
                ('http_status', models.CharField(default='N/A', max_length=3, verbose_name='HTTP Status')),
                ('product_vendor', models.CharField(default='N/A', max_length=255, verbose_name='Product Vendor')),
                ('product_name', models.CharField(default='N/A', max_length=255, verbose_name='Product Name')),
                ('product_version', models.CharField(default='N/A', max_length=255, verbose_name='Product Version')),
                ('product_type', models.CharField(default='N/A', max_length=255, verbose_name='Product Type')),
                ('product_trigger', models.CharField(default='N/A', max_length=5000, verbose_name='Product Trigger')),
                ('product_cveid', models.CharField(default='N/A', max_length=255, verbose_name='CVE-ID')),
                ('auth_form_trigger_ml', models.CharField(default='N/A', max_length=5000, verbose_name='ML Trigger of Form Auth')),
                ('auth_form_trigger_url', models.CharField(default='N/A', max_length=5000, verbose_name='URL Trigger of Form Auth')),
                ('auth_basic_trigger', models.CharField(default='N/A', max_length=5000, verbose_name='Trigger of BASIC Auth')),
                ('unnecessary_comments', models.CharField(default='N/A', max_length=5000, verbose_name='Unnecessary Comments')),
                ('unnecessary_contents', models.CharField(default='N/A', max_length=5000, verbose_name='Unnecessary Contents')),
                ('directory_index', models.CharField(default='N/A', max_length=5000, verbose_name='Directory Index')),
                ('error_messages', models.CharField(default='N/A', max_length=5000, verbose_name='Error Messages')),
                ('server_header', models.CharField(default='N/A', max_length=5000, verbose_name='Server Header')),
                ('log_path', models.CharField(default='N/A', max_length=1000, verbose_name='Log')),
                ('note', models.CharField(default='N/A', max_length=5000, verbose_name='Note')),
                ('invisible', models.BooleanField(default=False, verbose_name='Invisible')),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='industry',
            field=models.CharField(choices=[(1, 'ENERGY'), (2, 'MATERIALS'), (3, 'INDUSTRIALS'), (4, 'CONSUMER DISCRETIONARY'), (5, 'CONSUMER STAPLES'), (6, 'HEALTH CARE'), (7, 'FINANCIALS'), (8, 'INFORMATION TECHNOLOGY'), (9, 'COMMUNICATION SERVICES'), (10, 'UTILITIES'), (11, 'REAL ESTATE')], default='N/A', max_length=30, verbose_name='Industry'),
        ),
        migrations.AddField(
            model_name='organization',
            name='region',
            field=models.CharField(choices=[('Domestic', 'Domestic'), ('Abroad', 'Abroad')], default='Domestic', max_length=10, verbose_name='Region'),
        ),
        migrations.AddField(
            model_name='subdomain',
            name='auth_basic',
            field=models.BooleanField(default=False, verbose_name='Basic Authentication'),
        ),
        migrations.AddField(
            model_name='subdomain',
            name='auth_form',
            field=models.BooleanField(default=False, verbose_name='Form Authentication'),
        ),
        migrations.AddField(
            model_name='subdomain',
            name='cloud_type',
            field=models.CharField(default='Unknown', max_length=255, verbose_name='Cloud Type'),
        ),
        migrations.AddField(
            model_name='subdomain',
            name='production',
            field=models.BooleanField(default=True, verbose_name='Production Environment'),
        ),
        migrations.AddField(
            model_name='subdomain',
            name='url_origin',
            field=models.CharField(default='N/A', max_length=255, verbose_name='Top URL'),
        ),
        migrations.AlterField(
            model_name='domain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 8, 17, 35, 691271, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='organization',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 8, 17, 35, 690582, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='subdomain',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 12, 8, 17, 35, 691924, tzinfo=utc)),
        ),
    ]
