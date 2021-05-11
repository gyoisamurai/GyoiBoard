# Generated by Django 3.1.7 on 2021-05-03 02:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atd', '0027_auto_20210407_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='file_model',
            field=models.FileField(upload_to='atd/target/E44AXWsy3wr77MQ7bwZdqViLmmsxA4bgYebZQRo4hOHbD38U', validators=[django.core.validators.FileExtensionValidator(['h5'])], verbose_name='Model File (*.h5)'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file_x_test',
            field=models.FileField(upload_to='atd/target/E44AXWsy3wr77MQ7bwZdqViLmmsxA4bgYebZQRo4hOHbD38U', validators=[django.core.validators.FileExtensionValidator(['npz'])], verbose_name='X_test File (*.npz)'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file_x_train',
            field=models.FileField(upload_to='atd/target/E44AXWsy3wr77MQ7bwZdqViLmmsxA4bgYebZQRo4hOHbD38U', validators=[django.core.validators.FileExtensionValidator(['npz'])], verbose_name='X_train File (*.npz)'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file_y_test',
            field=models.FileField(upload_to='atd/target/E44AXWsy3wr77MQ7bwZdqViLmmsxA4bgYebZQRo4hOHbD38U', validators=[django.core.validators.FileExtensionValidator(['npz'])], verbose_name='y_test File (*.npz)'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file_y_train',
            field=models.FileField(upload_to='atd/target/E44AXWsy3wr77MQ7bwZdqViLmmsxA4bgYebZQRo4hOHbD38U', validators=[django.core.validators.FileExtensionValidator(['npz'])], verbose_name='y_train File (*.npz)'),
        ),
        migrations.AlterField(
            model_name='target',
            name='accuracy',
            field=models.FloatField(default=0.0, verbose_name='Accuracy'),
        ),
    ]
