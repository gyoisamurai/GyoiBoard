# Generated by Django 3.1.7 on 2021-03-29 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atd', '0010_scanresult_attack_method'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scanresult',
            old_name='task_id',
            new_name='scan_id',
        ),
    ]