from django.shortcuts import render
from django.http import JsonResponse
from eventCalendar.models import Events, Meetings, MeetingParticipation, Meetings_Computed
from datetime import datetime

# Create your views here.
def calendar(request):
    user = request.user
    #all_events = Events.objects.all()
    all_events = Events.objects.filter(userID = user)
    context = {
        "events":all_events,
    }
    return render(request,'eventCalendar/calendar1.html',context)

def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    userID = request.user
    event = Events(name=str(title), start=start, end=end, userID=userID)
    event.save()
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
    return render(request,'eventCalendar/calendar1.html')

#this will compute the available time frames of an invitation
def computeMeeting(self, parameter_list):
    pass