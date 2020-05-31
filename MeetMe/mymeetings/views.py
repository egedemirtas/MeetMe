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
        for k in meeting:
            try:
                tz = pytz.timezone('Europe/Istanbul')
                k.start = k.start.astimezone(tz)
                k.end = k.end.astimezone(tz)
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
    #meetingID=16     ###default

    #print(request)
    
    if(request.POST.get('ids')!=None):
        print("True")
        print(request.POST.get('ids'))
    else:
        print(request.POST.get('ids'))
        print("False")
        #print(request.POST['ids'] )   ##
        #MeetingEventIDs=request.POST['ids']   ## 
    if request.method == 'POST':
        print(request)    

    
    if request.method == 'POST':
        #print("Posted meeting id: "+request.POST.get('meetingID_r'))
        meetingID=request.POST['meetingID_r']
        print("-------------",meetingID)
        options=MeetingEvents.objects.filter(meetingID = meetingID)
        parc=MeetingParticipation.objects.get(meetingID = meetingID ,partID=user.id)
        """creatorID=Meetings.objects.get(meetingID = meetingID).creatorID
        if user.id == creatorID:
            creator=True
        else:
            creator=False    """
   
    #print(options[0].voteNumber)
    ## it should wait for response from the front
      
    
    if request.method == 'POST' and (request.POST.get('ids')!=None):
        print("After POST: ",meetingID)
        MeetingEventIDs=(request.POST['ids']).split(',')
        print(type(MeetingEventIDs))
        for MeetingEventID in MeetingEventIDs:
            result=MeetingEvents.objects.get(meetingEventID = MeetingEventID)
            result.voteNumber+=1
            result.save()
        parc.is_voted=True
        parc.save()
    
    return render(request,'mymeetings/voting.html', {'options': options,'meetingID_r':meetingID})
    
def decide(request):
    user=request.user

    if request.method == 'POST':
            #print("Posted meeting id: "+request.POST.get('meetingID_r'))
            meetingID=request.POST['meetingID_r']
            print("-------------",meetingID)
            options=MeetingEvents.objects.filter(meetingID = meetingID)
            parc=MeetingParticipation.objects.get(meetingID = meetingID ,partID=user.id)
            meeting=Meetings.objects.get(meetingID = meetingID)
            creatorID=meeting.creatorID
            if user.id == creatorID:
                creator=True
            else:
                creator=False

    if request.method == 'POST' and (request.POST.get('ids')!=None):
        print("After POST: ",meetingID)
        MeetingEventID=request.POST['ids']
        #print(type(MeetingEventID))
        meeting.is_decided=True


       

    