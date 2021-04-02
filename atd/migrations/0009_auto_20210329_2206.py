# Generated by Django 3.1.7 on 2021-03-29 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('atd', '0008_scansettingfgsm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scanresult',
            name='result',
        ),
        migrations.AddField(
            model_name='scanresult',
            name='task_id',
            field=models.CharField(default='', max_length=36),
        ),
        migrations.AlterField(
            model_name='scanresult',
            name='scan_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='atd.target'),
        ),
    ]