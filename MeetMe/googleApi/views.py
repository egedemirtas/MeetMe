from django.shortcuts import render
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from django.contrib import messages

def gCalendar(request):
    flow = InstalledAppFlow.from_client_secrets_file(
    'googleApi/client_secrets.json',
    scopes=['https://www.googleapis.com/auth/calendar'])
    auth_uri = flow.authorization_url()

    credentials=flow.run_local_server()
    print(credentials)                     ##
    service=build("calendar","v3",credentials=credentials)
    calendars=service.calendarList().list().execute()
    #calendar_id=calendars['items'][0]['id']  ##primary calendar also can be called via primary keyword
    events=service.events().list(calendarId='primary').execute()
    print(events)  ##
    events=str(events)
    messages.info(request,events)
    return render(request,'googleApi/a.html')

