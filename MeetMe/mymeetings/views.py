from django.shortcuts import render
from django.contrib.auth.models import User
from eventCalendar.models import Events, Meetings, MeetingParticipation, MeetingEvents
import calendar
from datetime import datetime, timedelta
import pytz
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
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
            if k.creatorID != user:
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
            print("-------------meetingid: ",meetingID)
            options=MeetingEvents.objects.filter(meetingID = meetingID)
            parcs=MeetingParticipation.objects.filter(meetingID = meetingID)
            meeting=Meetings.objects.get(meetingID = meetingID)
            creatorID=meeting.creatorID.id
            print("---Creator id: ",creatorID)
            print("---User id: ",user.id)
            if user.id == creatorID:
                creator=True
            else:
                creator=False

    if not creator:
        print("-----This is not a creator!!!!")
    else:    
        if request.method == 'POST' and (request.POST.get('ids')!=None):
            print("After POST: ",meetingID)
            MeetingEventID=request.POST['ids']
            #print(type(MeetingEventID))
            meeting.is_decided=True

            result=MeetingEvents.objects.get(meetingEventID = MeetingEventID)
            meeting.start=result.start
            meeting.end=result.end
            meeting.save()

            for parc in parcs:
                finalizeMeeting(parc.partID,meeting,request)


    return render(request,'mymeetings/decide.html', {'options': options,'meetingID_r':meetingID})

       
def finalizeMeeting(parcID,meeting,request):

    finalMail(request,parcID,meeting)

    parc=User.objects.get(id=parcID)
    event=Events(name=meeting.meetingName,start=meeting.start,end=meeting.end,userID=parc)
    event.save()

def finalMail(request,userID,meeting):
    current_site = get_current_site(request)
    
    creator=meeting.creatorID
    user=User.objects.get(id=userID)
    subject = 'We have news for a meeting you have been invited by '+ str(creator.username)
    message = render_to_string('mymeetings/finalMail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'meeting':  meeting,
                'token': urlsafe_base64_encode(force_bytes(user.password)),
            })
    user.email_user(subject, message)
       

def edit(request):
    meetingID=request.POST['meetingID_r']

    meeting = Meetings.objects.get(meetingID = meetingID)

    meetingEvents = MeetingEvents.objects.filter(meetingID = meeting)

    participants = MeetingParticipation.objects.filter(meetingID = meeting)

    context = {
        'meeting': meeting,
        'meetingEvents': meetingEvents,
        'participants': participants
    }
    return render(request,'mymeetings/editMeetingDemo.html', context)

def editComplete(request):
    pass