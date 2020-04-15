from django.urls import path
from . import views

urlpatterns = [
    path('calendar', views.calendar, name='calendar'),
    path('add_event', views.add_event, name='add_event'),
    path('update', views.update, name='update'),
    path('remove', views.remove, name='remove'),
    path('createMeeting', views.createMeeting, name='createMeeting'),
]