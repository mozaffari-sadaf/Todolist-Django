# Generated by Django 2.2.4 on 2019-09-02 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0010_todoitem_important'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='date_to_do',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='time_to_do',
            field=models.TimeField(null=True),
        ),
    ]
