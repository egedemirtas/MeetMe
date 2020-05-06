from django.urls import path
from . import views

urlpatterns = [
    path('mymeetings', views.myMeetings, name='mymeetings'),
    path('voting',views.voting, name='voting')
]