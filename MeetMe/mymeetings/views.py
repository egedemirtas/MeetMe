from django.shortcuts import render

# Create your views here.
def myMeetings(request):
    user = request.user
    #all_events = Events.objects.all()

    context = {
    }
    return render(request,'mymeetings/myMeetings.html',context)  ##testing
    #return render(request,'eventCalendar/addMeeting.html',context)