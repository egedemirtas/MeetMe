# Generated by Django 3.0.4 on 2020-04-22 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventCalendar', '0015_auto_20200422_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetings',
            name='beginLimit',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='meetings',
            name='endLimit',
            field=models.DateTimeField(null=True),
        ),
    ]
