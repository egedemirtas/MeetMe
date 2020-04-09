from django.shortcuts import render
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from django.contrib import messages
from eventCalendar.models import Events

def gCalendar(request):
    flow = InstalledAppFlow.from_client_secrets_file(
    'googleApi/client_secrets.json',
    scopes=['https://www.googleapis.com/auth/calendar'])
    auth_uri = flow.authorization_url()

    credentials=flow.run_local_server()
    #print(credentials)                     ##
    service=build("calendar","v3",credentials=credentials)
    calendars=service.calendarList().list().execute()
    events=service.events().list(calendarId='primary').execute() ##get all events
    #print(events)  ##
    #print(type(events))
    #events=str(events)
    #messages.info(request,events) 
    # #summary  title  
    for item in events['items']: 
        title=item['summary']
        start=item['start'].get('dateTime','NA')
        end=item['end'].get('dateTime','NA')
        if(start=='NA'):   ##For unspecified hour/minutes
            start=item['start']['date']
        if(end=='NA'):
            end=item['end']['date']
        #print(end.keys())
        print('{}, {}, {}'.format(title,start,end))
        event = Events(name=str(title), start=start, end=end)
        if not(Events.objects.filter(name=title,start=start,end=end).exists()): ##if it is not in db
            event.save()


    return render(request,'googleApi/a.html')
