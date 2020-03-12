from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import UserRegisterForm
from django.forms import inlineformset_factory

def register(request):
    """
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print('user created')
        else:
            messages.info(request, 'Passwords does not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            return redirect('register')
        else: 
            messages.warning(request, f'Account Name is taken')
    else:
        form = UserRegisterForm();
    return render(request, 'accounts/register.html', {'form':form})

def login(request):
     if request.method=='POST':
         username=request.POST['username']
         password=request.POST['password']
         user=auth.authenticate(username=username,password=password)
         if user is not None:
             auth.login(request,user)
             print('User login')
             return redirect('/')
         else:
             messages.info(request,'Invalid login please check your username and password')
             return redirect('login')
     else:
        return render(request,'accounts/login.html')     
