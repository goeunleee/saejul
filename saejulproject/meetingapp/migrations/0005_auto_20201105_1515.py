# Generated by Django 2.1 on 2020-11-05 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetingapp', '0004_auto_20201105_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='user_id',
            field=models.CharField(max_length=100),
        ),
    ]
