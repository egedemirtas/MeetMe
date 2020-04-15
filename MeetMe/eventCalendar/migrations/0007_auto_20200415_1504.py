# Generated by Django 3.0.4 on 2020-04-15 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventCalendar', '0006_auto_20200415_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='calendarID',
        ),
        migrations.AddField(
            model_name='events',
            name='userID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
