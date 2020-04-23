from threading import Timer
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
#from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes
from django.core.mail import send_mail
from MeetMe.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string

from eventCalendar.models import Events, Meetings, MeetingParticipation, Meetings_Computed
from datetime import datetime
import pytz
# Create your views here.
def calendar(request):
    user = request.user
    #all_events = Events.objects.all()
    all_events = Events.objects.filter(userID = user)
    context = {
        "events":all_events,
    }
    #return render(request,'eventCalendar/calendar1.html',context)
    return render(request,'eventCalendar/calendar.html',context)  ##testing

def profile(request):
    user = request.user
    #all_events = Events.objects.all()

    context = {
    }
    #return render(request,'eventCalendar/calendar1.html',context)
    return render(request,'eventCalendar/profile.html',context)      ##testing

def addMeeting(request):
    user = request.user
    #all_events = Events.objects.all()

    context = {
    }
    #return render(request,'eventCalendar/calendar1.html',context)  ##testing
    return render(request,'eventCalendar/addMeeting.html',context)

def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)

    start_unaware = datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
    start_aware = pytz.timezone('Europe/Istanbul').localize(start_unaware, is_dst=None)
    #start_utc = start_aware.astimezone(pytz.utc)

    end_unaware = datetime.strptime(end,"%Y-%m-%d %H:%M:%S")
    end_aware = pytz.timezone('Europe/Istanbul').localize(end_unaware, is_dst=None)
    #end_utc = end_aware.astimezone(pytz.utc)

    userID = request.user
    event = Events(name=str(title), start=start_aware, end=end_aware, userID=userID)
    event.save()

    #for debug
    user = request.user
    userEvents = Events.objects.filter(userID = user)
    for event in userEvents:
        print(event.start)
        """
        strippedEvent = str(event.start).split('+')[0]
        start_unaware = datetime.strptime(strippedEvent,"%Y-%m-%d %H:%M:%S")
        start_aware = pytz.timezone('Europe/Istanbul').localize(start_unaware, is_dst=None)
        """
        #this is the timezone to be converted
        tz = pytz.timezone('Europe/Istanbul')
        #convert event.start to tz timezone, event.start was utc before!!!
        start_Ist = event.start.astimezone(tz)
        print("retrieved from db:", start_Ist)
    
    data = {}
    return JsonResponse(data)

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)

def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

def createMeeting(request):
    #create a meeting
    meetingName = request.POST['meetingName']
    creatorID = request.user
    #beginLimit = request.POST["beginLimit"]
    #endLimit = request.POST["endLimit"]
    beginLimit = datetime(2019, 10, 9, 23, 55, 59, 342380)
    endLimit = datetime(2019, 10, 9, 23, 55, 59, 342380)
    meetingDuration = request.POST["meetingDuration"]
    meeting = Meetings.objects.create(meetingName = meetingName, creatorID = creatorID, beginLimit = beginLimit, endLimit = endLimit, meetingDuration = meetingDuration)

    #save the same meeting for attendance
    meetingID = meeting
    partUsername = request.POST["partUsername"]
    myList = partUsername.split(',')
    attendance = False
    for i in myList:
        meetingPart = MeetingParticipation.objects.create(meetingID = meetingID, partUsername = i, attendance = attendance)

    #save for computed meeting times
    """meetingIsActive = False
    computedStart = datetime(2019, 10, 9, 23, 55, 59, 342380)
    computedEnd = datetime(2019, 10, 9, 23, 55, 59, 342380)
    compMeeting = Meetings_Computed.objects.create(meetingID = meetingID, meetingIsActive = meetingIsActive, computedStart = computedStart, computedEnd = computedEnd)"""

    for part in myList:
        user = User.objects.get(username = part)
        print(user.username) ##
        invitation(request,user,creatorID)   
    ##start the timer
    #timer = Timer(120.0, computeMeeting(meeting.meetingID))
    args=[]
    args.append(meeting.meetingID)
    timer = Timer(120.0, computeMeeting,args)
    timer.start()
    ## check if all users have accepted 
        
    return render(request,'eventCalendar/calendar.html')

def invitation(request,user,creator):
    #token = default_token_generator.make_token(user)
    current_site = get_current_site(request)
    subject = 'Please Click the link if you want to accept event invitation by '+ str(creator.username)
    message = render_to_string('eventCalendar/acceptInvitation.html', {
                'user': user,
                'domain': current_site.domain,
                #'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #'token': account_activation_token.make_token(user),
            })
    user.email_user(subject, message)   
## if invitation accepted alter db accordingly
def acceptInvite(request):
    user=request.user
    meetingPart=MeetingParticipation.objects.get(partUsername = user.username)
    meetingPart.attendance=True
    meetingPart.save()
#this will compute the available time frames of an invitation
def computeMeeting(meetingID):
    print("Meeting computed! for id: "+str(meetingID))
