from django.urls import path
from .views import home_view,signup_view,signin_view,logout_view,weather_view

urlpatterns = [
    path('',home_view,name='home'),
    path('signup/',signup_view,name='signup'),
    path('signin/',signin_view,name='signin'),
    path('signout/',logout_view,name='signout'),
    path('weather/',weather_view,name='weather'),
]