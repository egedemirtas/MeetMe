from django.shortcuts import render
from django.http import JsonResponse
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
    return render(request,'eventCalendar/calendar1.html',context)

def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)

    start_unaware = datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
    start_aware = pytz.timezone('UTC').localize(start_unaware, is_dst=None)
    #start_utc = start_aware.astimezone(pytz.utc)
    
    end_unaware = datetime.strptime(end,"%Y-%m-%d %H:%M:%S")
    end_aware = pytz.timezone('UTC').localize(end_unaware, is_dst=None)
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
    meetingIsActive = False
    computedStart = datetime(2019, 10, 9, 23, 55, 59, 342380)
    computedEnd = datetime(2019, 10, 9, 23, 55, 59, 342380)
    compMeeting = Meetings_Computed.objects.create(meetingID = meetingID, meetingIsActive = meetingIsActive, computedStart = computedStart, computedEnd = computedEnd)
    return render(request,'eventCalendar/calendar.html')

#this will compute the available time frames of an invitation
def computeMeeting(self, parameter_list):
    pass