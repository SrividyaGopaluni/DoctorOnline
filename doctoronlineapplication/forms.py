from django import forms
from django.forms import ModelForm

from .models import User,Patient,Doctor,Service,Appointment


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)



class SignUpForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email__iexact=email).first()
        if user:
            if user.is_staff:
                user_role = "Staff"

            else:
                user_role = "Patient"
            raise forms.ValidationError(
                "{} with this email already exists, use another email.".format(
                    user_role
                )
            )
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise forms.ValidationError("Password should be minimum 6 characters long")

        if password != self.data.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match")
        return password


class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'time', 'name',)
        widgets = {
            'date': DateInput(),
        }




class PatientAddForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ()
        widgets = {
            'dateofbirth': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d')
                    }

    def __init__(self, *args, **kwargs):
        super(PatientAddForm, self).__init__(*args, **kwargs)
        self.fields['dateofbirth'].widget = DateInput()

class DoctorAddForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ()

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ('details','speciality')


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ()

