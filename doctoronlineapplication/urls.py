from django.conf.urls import url
from django.urls import path
from .views import *
from django.views.generic import TemplateView
from . import views

app_name = 'sma'

urlpatterns = [
    path("", homepage, name='homepage'),
    path("change-password/", change_password, name="change_password"),
    path("staff-login/", staffLogin, name='staffLogin'),
    path("mentor-login/", mentorLogin, name='mentorLogin'),

    path("staff-signup/", staffSignup, name='staffSignup'),
    path("mentor-signup/", mentorSignup, name='mentorSignup'),
    #path('appointment_form.html', views.new_appointment),
    path("new_appointment/",new_appointment,name='new_appointment'),
    path('doctor_details/',views.doctor_details,name='doctor_details'),
    path('pricing_details/',views.pricing_details,name='pricing_details'),
    path('view_bookings/',views.view_bookings,name='view_bookings'),
    path('booking_done/',views.booking_done,name = 'booking_done'),


    url(r'^info/(?P<user_type>[^\n]+)/$', views.view_doctors, name='view_doctors'),
    path('add/<str:user_type>/', views.add_doctors_or_patient, name='add_doctors_or_patient'),
    path('edit/<str:user_type>/<int:user_id>/', views.edit_doctor_or_patient, name='edit_doctor_or_patient'),
    path('delete/<str:user_type>/<int:user_id>/', views.delete_doctor_or_patient, name='delete_doctor_or_patient'),

    path('doctor_pdf/', views.doctor_summary_pdf, name='doctor_summary_pdf'),
    path('patient_pdf/', views.patient_summary_pdf, name='patient_summary_pdf'),

    path("logout/", user_logout, name='user_logout'),

]
