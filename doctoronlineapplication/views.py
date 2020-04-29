from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .access_decorators_mixins import patient_access_required, staff_access_required
from django.db import connection,transaction

# Create your views here.

def staffSignup(request):
    if request.method == "GET":
        return render(request, "sma/staff_signup.html", {})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("email"),
                is_staff=True, role='staff'
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return redirect(reverse("sma:homepage",))
        else:
            return render(
                request, "sma/staff_signup.html", {"errors": form.errors}
            )


def mentorSignup(request):
    if request.method == "GET":
        return render(request, "sma/mentor_signup.html", {})

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("email"),
                is_patient=True, role="patient",
            )
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            login(request, user)
            return redirect(reverse("sma:homepage",))
        else:
            return render(
                request, "sma/mentor_signup.html", {"errors": form.errors}
            )


def mentorLogin(request):
    if request.method == "GET":
        return render(request, "sma/mentor_login.html", {})

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password,)
            if user is None:
                return render(
                    request,
                    "sma/mentor_login.html",
                    {"errors": {"account_error": ["Invalid email or password"]}},
                )

            elif user is not None:
                if user.is_active and user.is_patient:
                    login(request, user)
                    return HttpResponseRedirect(reverse("sma:homepage",))
                elif user.is_active and user.is_patient is False:
                    return render(
                        request,
                        "sma/mentor_login.html",
                        {
                            "errors": {
                                "account_error": ["Email is not associated with Patient"]
                            }
                        },
                    )

                else:
                    return HttpResponse(
                        "# your account is inactive contact admin for details user@example.com"
                    )

            else:
                pass
        else:
            return render(request, "sma/mentor_login.html", {"errors": form.errors})




def staffLogin(request):
    if request.method == "GET":
        return render(request, "sma/staff_login.html", {})

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=email, password=password,)
            if user is None:
                return render(
                    request,
                    "sma/staff_login.html",
                    {"errors": {"account_error": ["Invalid email or password"]}},
                )

            elif user is not None:
                if user.is_active and user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect(reverse("sma:homepage",))
                elif user.is_active and user.is_patient is False:
                    return render(
                        request,
                        "sma/staff_login.html",
                        {
                            "errors": {
                                "account_error": ["Email is not associated with Staff"]
                            }
                        },
                    )

                else:
                    return HttpResponse(
                        "# your account is inactive contact admin for details user@example.com"
                    )

            else:
                pass
        else:
            return render(request, "sma/staff_login.html", {"errors": form.errors})


def change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'GET':
        return render(request, "sma/password_change_form.html", {"form": form})
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return render(
                request, "sma/password_change_done.html", {}
            )
        return render(
            request, "sma/password_change_form.html", {"errors": form.errors}
        )



def homepage(request):
    #print('yessss')
    # return HttpResponse("test sma")
    return render(request, "sma/landing_page.html", {})


def user_logout(request):
    logout(request)
    return redirect(reverse("sma:homepage"))

#book appointment done:
@login_required
def booking_done(request):
    booking_done = Appointment.objects.filter()
    return render(request,'sma/booking_done.html',{'booking_done':booking_done})

#For appointment booking:
@login_required
def new_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"sma/booking_done.html",{})
    else:
        form = AppointmentForm()
    return render(request, "sma/appointment_form.html", {'form': form})

@login_required
def doctor_details(request):
   session = Doctor.objects.filter()
   return render(request,'sma/doctor_details.html',{'doctor_details': session})

@login_required
def pricing_details(request):
    price = Service.objects.filter()
    return render(request,'sma/pricing_details.html',{'pricing_details':price})


def view_bookings(request):
    #reserve = Appointment.objects.filter(name=request.user)
    reserve = Appointment.objects.filter()
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaasdfggggggggwrv gggggggggg ggggggggggg")
    print(request.user)
    return render(request,'sma/view_bookings.html',{'reserve':reserve})


def view_doctors(request,user_type):
    if user_type == 'patient':
        patients_list = Patient.objects.all()
        print("patients")
        print(patients_list)
        return render(request,'sma/staff_doctor_list.html',{'list_info': patients_list ,'user_type':user_type})

    elif user_type == 'doctor':
        doctors_list = Doctor.objects.all()
        print("doctors")
        print(doctors_list)
        return render(request,'sma/staff_doctor_list.html',{'list_info':doctors_list,'user_type':user_type})




def add_doctors_or_patient(request,user_type):

    if user_type == 'doctor':

        if request.method == "GET":
            form = DoctorAddForm()
            return render(request,'sma/doctor_patient_add.html',{'form':form})
        if request.method == "POST":
            form = DoctorAddForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form = DoctorAddForm()
                return render(request,'sma/doctor_patient_add.html',{'form':form})

    elif user_type == 'patient':

        if request.method == "GET":
            form = PatientAddForm()
            return render(request,'sma/doctor_patient_add.html',{'form':form})
        if request.method == "POST":
            form = PatientAddForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form = PatientAddForm()
                return render(request,'sma/doctor_patient_add.html',{'form':form})
        print(user_type)
    return redirect(reverse('sma:view_doctors',kwargs={'user_type':user_type}))


def edit_doctor_or_patient(request, user_type, user_id):
    if user_type == 'doctor':
        doctor_data = get_object_or_404(Doctor, pk=user_id)
        if request.method == "GET":
            form = DoctorForm(instance=doctor_data)
            return render(request, 'sma/doctor_patient_edit.html', {'form': form})
        if request.method == "POST":
            form = DoctorForm(request.POST, instance=doctor_data)
            if form.is_valid():
                form.save()
            else:
                form = DoctorForm(instance=doctor_data)
                return render(request, 'sma/doctor_patient_edit.html', {'form': form})


    elif user_type == 'patient':
        patient_data = get_object_or_404(Patient, pk=user_id)
        if request.method == "GET":
            form = PatientForm(instance=patient_data)
            return render(request, 'sma/doctor_patient_edit.html', {'form': form})
        if request.method == "POST":
            form = PatientForm(request.POST, instance=patient_data)
            if form.is_valid():
                form.save()
            else:
                form = PatientForm(instance=patient_data)
                return render(request, 'sma/doctor_patient_edit.html', {'form': form})
    return redirect(reverse('sma:view_doctors', kwargs={'user_type': user_type}))




def delete_doctor_or_patient(request, user_type, user_id):
    if user_type == 'doctor':
        doctor = get_object_or_404(Doctor, pk=user_id)
        doctor.delete()
    elif user_type == 'patient':
        patient = get_object_or_404(Patient, pk=user_id)
        patient.delete()
    return redirect(reverse('sma:view_doctors', kwargs={'user_type': user_type}))




from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template


def doctor_summary_pdf(request):
    doctor = Doctor.objects.all()
    context = {'doctor': doctor, }
    template = get_template('sma/doctor_summary_pdf.html')
    html = template.render(context)
    pdf = render_to_pdf('sma/doctor_summary_pdf.html', context)
    return pdf


def patient_summary_pdf(request):
    patient = Patient.objects.all()
    context = {'patient': patient, }
    template = get_template('sma/patient_summary_pdf.html')
    html = template.render(context)
    pdf = render_to_pdf('sma/patient_summary_pdf.html', context)
    return pdf





