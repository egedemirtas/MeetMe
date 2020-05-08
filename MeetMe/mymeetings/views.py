from django.shortcuts import render
from django.contrib.auth.models import User
from eventCalendar.models import Events, Meetings, MeetingParticipation, MeetingEvents
import calendar
from datetime import datetime, timedelta
import pytz
# Create your views here.
def myMeetings(request):
    user = request.user
    partMeetings =[]
    #all_events = Events.objects.all()

    #get all the meetings that the current user is the creator
    userMeetings = Meetings.objects.filter(creatorID = user)

    #get all the participated meetings (all the meetings that we have been invited)
    #first find the ids of the meetings that ve have been invited to
    meetingIDs = MeetingParticipation.objects.filter(partID = user.id)

    #search these meeting ids in meetings
    for i in meetingIDs:
        meeting = Meetings.objects.filter(meetingID = i.meetingID.meetingID)
        print("current meetings is:", meeting[0].meetingID)
        print("current start is:", meeting[0].start)
        print("current end is:", meeting[0].end)
        for k in meeting:
            try:
                tz = pytz.timezone('Europe/Istanbul')
                k.start = k.start.astimezone(tz)
                k.end = k.end.astimezone(tz)
                print("After current start is:", k.start)
                print("After current end is:", k.end)
                creatorUsername = User.objects.filter(id = k.creatorID.id)
                partMeetings.append([k, creatorUsername[0].username])
            except AttributeError:
                creatorUsername = User.objects.filter(id = k.creatorID.id)
                partMeetings.append([k, creatorUsername[0].username])
    
    #convert time for the creator's meetings
    for i in userMeetings:
        try:
            #this is the timezone to be converted
            tz = pytz.timezone('Europe/Istanbul')
            #convert event.start to tz timezone, event.start was utc before!!!
            i.start = i.start.astimezone(tz)
            i.end = i.end.astimezone(tz)
        except AttributeError:
            continue
    
    context = {
        'createdMeetings': userMeetings,
        'partMeetings': partMeetings,
    }
    return render(request,'mymeetings/myMeetings.html',context)  ##testing
    #return render(request,'eventCalendar/addMeeting.html',context)



def voting(request):
    user=request.user
    #meetingID=16 ###
    meetingID=request.POST['meetingID_r']
    print("-------------",meetingID)
    options=MeetingEvents.objects.filter(meetingID = meetingID)
    parc=MeetingParticipation.objects.get(meetingID = meetingID ,partID=user.id)
    #print(options[0].voteNumber)
    ## it should wait for response from the front
    '''
    if request.method=='POST':
        MeetingEventID=request.POST['id']
        result=MeetingEvents.objects.get(MeetingEventID = 1)
        result.voteNumber+=1
        result.save()
        parc.is_voted=True
        parc.save()
    '''
    return render(request,'mymeetings/voting.html', {'options': options})
    