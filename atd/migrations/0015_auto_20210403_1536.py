# Generated by Django 3.1.7 on 2021-04-03 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atd', '0014_auto_20210403_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='author',
            field=models.CharField(default='test', max_length=255, verbose_name='Author'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='target',
            name='author',
            field=models.CharField(default=1, max_length=255, verbose_name='Author'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='target',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Model name'),
        ),
    ]
