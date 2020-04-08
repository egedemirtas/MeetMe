from django.urls import path

from . import views
#from django.contrib.auth import views as auth_views
app_name = "accounts"
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login')
    #auth_views.login.as_view(template_name= 'users/login.html')path('logout/', auth_views.LogoutView.as_view(template_name= 'users/logout.html'), name= 'logout')
]
