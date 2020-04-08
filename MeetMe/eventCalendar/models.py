from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Calendar(models.Model):
    calendarID = models.AutoField(primary_key=True)
    calendarName = models.CharField(max_length=255, null=True, blank=True)
    userID = models.ForeignKey(User, null=True, on_delete = models.CASCADE)

class Events(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    calendarID = models.ForeignKey(Calendar, null=True, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Meetings(models.Model):
    meetingID = models.AutoField(primary_key=True)
    invitedUserID = models.IntegerField(null=True)
    sentCalendarID = models.IntegerField(null=True)
    awr = models.CharField(max_length=255, null=True, blank=True)
    acceptedCalendarID = models.IntegerField(null=True)
    computedStart = models.DateTimeField(null=True)
    computedEnd = models.DateTimeField(null=True)


