from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#this stores every user's events on their calendar
class Events(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
#data entered here when a meeting is created by the user
class Meetings(models.Model):
    meetingID = models.AutoField(primary_key=True)
    meetingName = models.CharField(max_length=255, null=True, blank=True)
    creatorID = models.ForeignKey(User, null=True, on_delete = models.CASCADE)
    beginLimit = models.DateTimeField(null=True)
    endLimit = models.DateTimeField(null=True)
    meetingDuration = models.CharField(max_length=255, null=True, blank=True)
#this is to record the users and the participation of a recorded meeting
class MeetingParticipation(models.Model):
    meetingParID = models.AutoField(primary_key=True)
    meetingID = models.ForeignKey(Meetings, null=True, on_delete = models.CASCADE)
    partUsername = models.CharField(max_length=255, null=True, blank=True)
    attendance = models.BooleanField(default=False)
#this is to store the computed possible meeting time frame for a meeting
class Meetings_Computed(models.Model):
    meetingCompID = models.AutoField(primary_key=True)
    meetingID =  models.ForeignKey(Meetings, null=True, on_delete = models.CASCADE)
    meetingIsActive = models.BooleanField(default=False)
    computedStart = models.DateTimeField(null=True)
    computedEnd = models.DateTimeField(null=True)