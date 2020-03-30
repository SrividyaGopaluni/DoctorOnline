from django.urls import path
from .views import *
from . import views

app_name = 'sma'

urlpatterns = [
    path("", homepage, name='homepage'),
    path("change-password/", change_password, name="change_password"),
    path("staff-login/", staffLogin, name='staffLogin'),
    path("mentor-login/", mentorLogin, name='mentorLogin'),

    path("staff-signup/", staffSignup, name='staffSignup'),
    path("mentor-signup/", mentorSignup, name='mentorSignup'),

    path("logout/", user_logout, name='user_logout'),

]
