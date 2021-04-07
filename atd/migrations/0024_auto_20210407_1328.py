# Generated by Django 3.1.7 on 2021-04-07 04:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atd', '0023_auto_20210407_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scansettingcnw',
            name='use_dataset_num',
        ),
        migrations.RemoveField(
            model_name='scansettingfgsm',
            name='use_dataset_num',
        ),
        migrations.RemoveField(
            model_name='scansettingjsma',
            name='use_dataset_num',
        ),
        migrations.AddField(
            model_name='extevasioncnw',
            name='dataset_num',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extevasionfgsm',
            name='dataset_num',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extevasionjsma',
            name='dataset_num',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scansettingcnw',
            name='dataset_num',
            field=models.IntegerField(default=100, verbose_name="Using dataset's number"),
        ),
        migrations.AddField(
            model_name='scansettingfgsm',
            name='dataset_num',
            field=models.IntegerField(default=100, verbose_name="Using dataset's number"),
        ),
        migrations.AddField(
            model_name='scansettingjsma',
            name='dataset_num',
            field=models.IntegerField(default=100, verbose_name="Using dataset's number"),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file_model',
            field=models.FileField(upload_to='atd/target/h9ge5uJTLwKp8pJ1bx52XCcZAALQLpFfDHyWZvf94gEQ7KHj', validators=[django.core.validators.FileExtensionValidator(['h5'])], verbose_name='Model File (*.h5)'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file_x_test',
            field=models.FileField(upload_to='atd/target/h9ge5uJTLwKp8pJ1bx52XCcZAALQLpFfDHyWZvf94gEQ7KHj', validators=[django.core.validators.FileExtensionValidator(['npz'])], verbose_name='X_test File (*.npz)'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file_x_train',
            field=models.FileField(upload_to='atd/target/h9ge5uJTLwKp8pJ1bx52XCcZAALQLpFfDHyWZvf94gEQ7KHj', validators=[django.core.validators.FileExtensionValidator(['npz'])], verbose_name='X_train File (*.npz)'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file_y_test',
            field=models.FileField(upload_to='atd/target/h9ge5uJTLwKp8pJ1bx52XCcZAALQLpFfDHyWZvf94gEQ7KHj', validators=[django.core.validators.FileExtensionValidator(['npz'])], verbose_name='y_test File (*.npz)'),
        ),
        migrations.AlterField(
            model_name='fileupload',
            name='file_y_train',
            field=models.FileField(upload_to='atd/target/h9ge5uJTLwKp8pJ1bx52XCcZAALQLpFfDHyWZvf94gEQ7KHj', validators=[django.core.validators.FileExtensionValidator(['npz'])], verbose_name='y_train File (*.npz)'),
        ),
    ]