from django.shortcuts import render
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
                is_patient=True, role="mentor",
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