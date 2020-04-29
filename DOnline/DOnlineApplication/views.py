from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.views.generic import CreateView

from .forms import AppointmentForm
from .models import Appointment

# Create your views here.

def home(request):
    return render(request,'home.html',{})

def contact(request):
    if request.method =="POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']
        return render(request, 'contact.html', {'message-name':message_name})

        send_mail(
            message_name,
            message,
            message_email,
            ['srividyagopaluni@gmail.com'],
            fail_silently=False,

            )

    else:
        return render(request,'contact.html',{})




'''class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm'''

def new_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('DOnlineApplication:contact')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form})



