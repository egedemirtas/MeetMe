from django.shortcuts import render
from eventCalendar.models import Events, Meetings, MeetingParticipation, MeetingEvents

# Create your views here.
def myMeetings(request):
    user = request.user
    #all_events = Events.objects.all()

    context = {
    }
    return render(request,'mymeetings/myMeetings.html',context)  ##testing
    #return render(request,'eventCalendar/addMeeting.html',context)
def voting(request):
    user=request.user
    meetingID=16 ###
    #meetingID=request.POST('meetingID_r')
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
    