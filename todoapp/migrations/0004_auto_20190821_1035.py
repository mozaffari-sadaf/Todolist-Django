# Generated by Django 2.2.4 on 2019-08-21 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0003_auto_20190820_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='time_to_do',
            field=models.DateTimeField(),
        ),
    ]
