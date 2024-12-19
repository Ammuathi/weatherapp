from django.shortcuts import render,redirect
from . models import CustomUser
from django.contrib import messages
from django.contrib.auth import logout,authenticate,login
import requests
import datetime
from django. contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
load_dotenv()



# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        errors={}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if CustomUser.objects.filter(email=email).exists():
            errors["email"]="email do not match"
        if CustomUser.objects.filter(username=username).exists():
            errors['username']="username already exists"
        if password!=confirm_password:
            errors['confirm_password']="Password does not match"
        
        if errors:
            return render(request,"signup.html",{'errors':errors})

        user = CustomUser.objects.create_user(
        email=email,
        username=username,
        password = password)

            # user.set_password(password)
            # user.save()

        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('signin')
    
    return render(request,'signup.html')

def signin_view(request):
    if request.method == 'POST':
        errors={}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            print(user,"ddddddd")
            login(request,user)
            return redirect('weather')
        
        else:
            errors['user'] = "user not found"
            #  messages.error(request, 'wrong password')
    return render(request,'signin.html')

def logout_view(request):
    logout(request)
    return redirect('signin')

def home_view(request):
    return render(request,'home.html')

# def weather(request):
@login_required(login_url = 'signin')
def weather_view(request):
    # return render(request,'weather.html')
    errors={}
    if 'city' in request.POST:
        city= request.POST.get('city')
    else:
        city = 'palakkad'

    APP_ID = os.getenv('APP_ID')   
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city }&appid={APP_ID}"

    PARAMS = {'units':'metric'}
    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()


        return render(request, 'weather.html',{
            'description':description,
            'icon':icon,
            'temp':temp,
            'day':day,
            'city':city,
            'exception_occured':False,
        })
    except KeyError:
        exception_occured = True  
        errors['weather'] = 'entered data is not availbale to API'
        # messages.error(request,'entered data is not availbale to API')
        day = datetime.date.today()

    return render(request,'weather.html', {
        'description':'clear sky',
            'icon':'01d',
            'temp':25,
            'day':day,
            'city':'palakkad',
            'exception_occured':exception_occured,
        })
    