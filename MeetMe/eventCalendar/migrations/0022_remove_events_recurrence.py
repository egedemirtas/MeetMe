# Generated by Django 3.0.4 on 2020-06-01 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventCalendar', '0021_events_recurrence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='recurrence',
        ),
    ]
