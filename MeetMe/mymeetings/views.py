from django.shortcuts import render
from eventCalendar.models import Events, Meetings, MeetingParticipation, MeetingEvents

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
    for i in range(len(meetingIDs)):
        meeting = Meetings.objects.filter(meetingID = meetingIDs[i].meetingID.meetingID)
        partMeetings.append(meeting)

    for i in partMeetings:
        print(i[0].note)

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
    print(meetingID)
    options=MeetingEvents.objects.filter(meetingID = meetingID)
    parc=MeetingParticipation.objects.get(meetingID = meetingID ,partID=user.id)
    #print(options[0].voteNumber)
    ## it should wait for response from the front
    if request.method=='POST':
        MeetingEventID=request.POST['id']
        result=MeetingEvents.objects.get(MeetingEventID = 1)
        result.voteNumber+=1
        result.save()
        parc.is_voted=True
        parc.save()

    return render(request,'mymeetings/voting.html', {'options': options})
    