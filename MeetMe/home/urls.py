from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    #path("upper_menu", views.upper_menu, name="upper_menu")
]