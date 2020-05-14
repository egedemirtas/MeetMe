from threading import Timer
from django.shortcuts import render, redirect
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

from eventCalendar.models import Events, Meetings, MeetingParticipation, MeetingEvents
from datetime import datetime, timedelta
import pytz
from operator import itemgetter
from django.contrib import auth
# Create your views here.
def calendar(request):
    user = request.user
    #all_events = Events.objects.all()
    all_events = Events.objects.filter(userID = user)
    myList =[]
    for i in all_events:
        #this is the timezone to be converted
        tz = pytz.timezone('Europe/Istanbul')
        #convert event.start to tz timezone, event.start was utc before!!!
        q = i.start.astimezone(tz)
        x = str(q)
        xList = x.split()
        y = xList[0] + 'T' + xList[1].split('+')[0]

        q = i.end.astimezone(tz)
        k = str(q)
        kList = k.split()
        z = kList[0] + 'T' + kList[1].split('+')[0]

        m = i.name
        l = i.id

        myList.append([y,z,m,l])

    context = {
        "events":myList,
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

def polls(request):
    user = request.user
    #all_events = Events.objects.all()

    context = {
    }
    #return render(request,'eventCalendar/calendar1.html',context)  ##testing
    return render(request,'eventCalendar/votepolls.html',context)

def myMeetings(request):
    user = request.user
    #all_events = Events.objects.all()

    context = {
    }
    #return render(request,'eventCalendar/calendar1.html',context)  ##testing
    return render(request,'eventCalendar/myMeetings.html',context)
def addEvent(request):
    user = request.user
    #all_events = Events.objects.all()

    context = {
    }
    return render(request,'eventCalendar/addEvent.html',context)  ##testing
    #return render(request,'eventCalendar/addMeeting.html',context)

def add_event(request):

    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    print("this is start:", start)
    print("this is end:", end)
    print("this is title:", title)

    start_unaware = datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
    start_aware = pytz.timezone('Europe/Istanbul').localize(start_unaware, is_dst=None)
    #start_utc = start_aware.astimezone(pytz.utc)

    end_unaware = datetime.strptime(end,"%Y-%m-%d %H:%M:%S")
    end_aware = pytz.timezone('Europe/Istanbul').localize(end_unaware, is_dst=None)
    #end_utc = end_aware.astimezone(pytz.utc)

    userID = request.user
    #event = Events(name=str(title), start=start, end=end, userID=userID)
    event = Events(name = title, start=start_aware, end=end_aware, userID=userID)
    event.save()

    """
    #delete these if you want to use above part
    if request.method == 'POST':
        start=request.POST['start']
        end=request.POST['end']
        title = request.POST['title']
        print(start)

        userID = request.user
        #event = Events(name=str(title), start=start_aware, end=end_aware, userID=userID)
        event = Events(name=str(title), start=start, end=end, userID=userID)
        event.save()
        return redirect('addEvent')

    #for debug
    user = request.user
    userEvents = Events.objects.filter(userID = user)
    for event in userEvents:
        print(event.start)
        #this is the timezone to be converted
        tz = pytz.timezone('Europe/Istanbul')
        #convert event.start to tz timezone, event.start was utc before!!!
        start_Ist = event.start.astimezone(tz)
        print("retrieved from db:", start_Ist)
    """
    data = {}
    return JsonResponse(data)

    render(request, 'eventCalendar/addEvent.html')

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
    print("deleted id is:", id)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

def createMeeting(request):
    #these are dummy, data must be received from request
    #creatorID = User.objects.get(username = "efehan") #user = request.user
    creatorID = request.user
    meetingName = "Internship Interview1"
    is_decided = False
    location = "Istanbul/Kadikoy"
    note = "meet at starbucks"
    participants = ["kobee", "dwayne"]
    recurrence = "Weekly"
    a = datetime(2020, 5, 3, 9, 30, 00, 0)
    b = datetime(2020, 5, 3, 10, 30, 00, 0)
    c = datetime(2020, 5, 3, 11, 00, 00, 0)
    d = datetime(2020, 5, 3, 14, 00, 00, 0)
    e = datetime(2020, 5, 3, 17, 00, 00, 0)
    f = datetime(2020, 5, 3, 23, 00, 00, 0)
    meetingIntervals = [[a, b], [c, d], [e, f]]


    #create meeting: participants is unnecessary
    meeting = Meetings.objects.create(creatorID=creatorID, meetingName=meetingName, 
                is_decided=is_decided, location=location, note=note, participants=None, recurrence=recurrence)
    meeting.save()
    print("saved meeting id is:", meeting.pk)

    #save the time intervals for the meeting
    for i in range(len(meetingIntervals)):
        meetingsEvents = MeetingEvents.objects.create(meetingID = meeting, start=meetingIntervals[i][0],end=meetingIntervals[i][1],voteNumber=0)
        meetingsEvents.save()

    #save for meetings attendance
    for i in participants:
        partid = User.objects.get(username=i)#get the id of participant
        #for now since noone voted, meetingEventID is null(None)
        meetingParticipation = MeetingParticipation.objects.create(meetingID = meeting, meetingEventID=None, partUsername = i, partID = partid.id, is_voted=False)
    
    #invited meeting list is unnecessary
    
    #send invitations
    for part in participants:
        user = User.objects.get(username = part)
        print(user.username)
        invitation(request,user,creatorID)

    ##start the timer
    #timer = Timer(120.0, computeMeeting(meeting.meetingID))
    args=[]
    args.append(request)
    args.append(participants)
    args.append(creatorID)
    args.append(meeting.pk)
    timer = Timer(60.0, invitationReminder, args)
    timer.start()

    '''
    meetingName = request.POST['meetingName']
    creatorID = request.user
    user = User.objects.get(username = "test1")

    invitation(request,user,creatorID)####

    user2 = User.objects.get(username = "test2")
    invitation(request,user2,creatorID)

    beginLimit = request.POST["beginLimit"]
    endLimit = request.POST["endLimit"]
    print(beginLimit)
    print(endLimit)
    meetingDuration = request.POST["meetingDuration"]
    meeting = Meetings.objects.create(meetingName = meetingName, creatorID = creatorID, beginLimit = beginLimit, endLimit = endLimit, meetingDuration = meetingDuration)

    #save the same meeting for attendance
    meetingID = meeting
    partUsername = request.POST["partUsername"]
    myList = partUsername.split(',')
    attendance = False
    for i in myList:
        meetingPart = MeetingParticipation.objects.create(meetingID = meetingID, partUsername = i, attendance = attendance)
    '''

    """
    ##start the timer
    #timer = Timer(120.0, computeMeeting(meeting.meetingID))
    args=[]
    args.append(meeting.meetingID)
    timer = Timer(90.0, computeMeeting,args)
    timer.start()
    ## check if all users have accepted
    """
    return redirect('calendar')

def invitationReminder(request,participants,creator,meetingID):
    #token = default_token_generator.make_token(user)
    meeting = Meetings.objects.filter(meetingID=meetingID)#find the meeting object
    if meeting[0].is_decided == False:#send reminder if the meeting hasnt been decided yet
        for part in participants:
            find_isVoted = MeetingParticipation.objects.filter(meetingID = meeting[0], partUsername=part)#find if the part has voted yet
            print(find_isVoted)
            if find_isVoted[0].is_voted == False:#send reminder only if the part hasnt voted
                partObj = User.objects.get(username=part)
                current_site = get_current_site(request)
                subject = 'This is a reminder that you have been invited by '+ str(creator.username) +" to participate in a poll."
                message = render_to_string('eventCalendar/acceptInvitation.html', {
                            'user': partObj,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(partObj.pk)),
                            'token': urlsafe_base64_encode(force_bytes(partObj.password)),
                        })
                partObj.email_user(subject, message)





def invitation(request,user,creator):
    #token = default_token_generator.make_token(user)
    current_site = get_current_site(request)
    subject = 'Please Click the link if you want to accept event invitation by '+ str(creator.username)
    message = render_to_string('eventCalendar/acceptInvitation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': urlsafe_base64_encode(force_bytes(user.password)),

            })
    user.email_user(subject, message)

## if invitation accepted alter db accordingly
def acceptInvite(request,uidb64,token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    uid = force_text(urlsafe_base64_decode(uidb64))
    if user is not None and user.password==force_text(urlsafe_base64_decode(token)):
             auth.login(request,user)
             print('User login')
             return redirect('/eventCalendar/calendar')
    else:
        print("Fatal Error")

    #meetingPart=MeetingParticipation.objects.get(partUsername = user.username)
    #meetingPart.attendance=True
    #meetingPart.save()

"""
#this will compute the available time frames of an invitation
def computeMeeting(currentID):
    print(currentID,"------------------------------")

    #get participants in a list
    participants = MeetingParticipation.objects.filter(meetingID=currentID, attendance=True).values_list('partUsername',flat=True)
    print("these are participants",participants)
    #get paticipants' id in alists
    idList = []
    for i in participants:
        current = User.objects.filter(username = i).values_list('id',flat=True)
        idList.append(current[0])
    print("this is id list", idList)

    #this is the current meeting: begin&end bounds, creatorID, duration
    requestedInfo = Meetings.objects.filter(meetingID=currentID)
    print("this is requestedINfo",requestedInfo)

    #this is the duration of the meeting
    now = datetime.now()
    duration = requestedInfo[0].meetingDuration
    duration = int(duration)
    print("this is duration in int: ",duration) #this will be used if we want to add 30min to a datetime object
    now1 = now + timedelta(minutes = duration)
    durTime = now1 - now #this will be used if we want to compare 2 hours
    print("this is duration in time:",durTime)

    #this is the begin and end bounds of the meeting
    tz = pytz.timezone('Europe/Istanbul')
    beginBound = requestedInfo[0].beginLimit
    beginBound = beginBound.astimezone(tz)
    endBound = requestedInfo[0].endLimit
    endBound = endBound.astimezone(tz)
    print("beginbound is:", beginBound)
    print("endbound is:", endBound)

    #this will be used to store events for each participant
    eventList = []
    #from the idList list, get their each participants' events (their start datetime should be ordered)
    #first add the creator's id in list
    idList.append(requestedInfo[0].creatorID.id)
    print("This is id of everyone:",idList)
    for i in idList:
        arr = Events.objects.filter(userID = i).order_by('start')
        eventList.append(arr)
    print(eventList)

    allEvents = []
    for i in eventList:
        print("User's events:")
        for j in i:#in a <QueryList>
            start_tz = j.start.astimezone(tz)
            end_tz = j.end.astimezone(tz)
            print(start_tz, "------",end_tz)
            anEvent = [start_tz, end_tz]
            allEvents.append(anEvent)

    print("----------------------------------------------")
    allEvents.sort(key=itemgetter(0))#now all the evnts from all the users are sorted by starting times
    for i in allEvents:
        print("An Event:")
        for j in i:
            print(j)

    h = 0
    while h < len(allEvents)-1:
        end1 = allEvents[h][1]
        start2 = allEvents[h+1][0]
        if end1 > start2:
            end2 = allEvents[h+1][1]
            if end2 < end1:
                allEvents.pop(h+1)
                h-=1
            else:
                allEvents[h][1] = end2
        h+=1

    print("----------------------------------------------")
    for i in allEvents:
        print("An Event:")
        for j in i:
            print(j)

    solutions = []
    print("----------------------------------------------")
    for i in range(len(allEvents)-1):
        end1 = allEvents[i][1]
        start2 = allEvents[i+1][0]
        if start2 > end1 and end1 >= beginBound and start2 < endBound:
            solutions.append([end1, start2])

    for i in solutions:
        for j in i:
            print(j)

    meetingName = Meetings.objects.filter(meetingID=currentID).values_list('meetingName',flat=True)
    print("this is meeting name",meetingName[0])
    print("this is solution start-end",solutions[0][0], solutions[0][1])

    for i in idList:
        part = User.objects.get(id =i)
        event = Events.objects.create(name = meetingName[0], start=solutions[0][0], end=solutions[0][1], userID=part)
"""
