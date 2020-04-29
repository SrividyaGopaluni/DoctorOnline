
from django.urls import path,re_path
from . import views
from django.conf.urls import url

app_name = 'DOnlineApplication'
urlpatterns = [
    path('',views.home,name='home'),
    path('contact.html',views.contact,name="contact"),
    path('appointment_form.html', views.new_appointment),
]