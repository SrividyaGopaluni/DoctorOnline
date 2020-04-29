from django import forms
from django.forms import ModelForm
from .models import Appointment
from bootstrap_datepicker_plus import DateTimePickerInput
from bootstrap_datepicker_plus import DatePickerInput


'''class DateInput(forms.DateInput):
    input_type = 'date'''

'''class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'timeslot', 'patient_name',]
        widgets = {
            'date': DateInput(),
        }
'''
#from datetimewidget.widgets import DateTimeWidget


'''class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'timeslot', 'patient_name',)
        widgets = {
            'date': DatePickerInput(
                attrs={'id': 'date'},
                options={
                    'minView': 2,  # month view
                    'maxView': 3,  # year view
                    'weekStart': 1,
                    'todayHighlight': True,
                    'format': 'yyyy-mm-dd',
                    'daysOfWeekDisabled': [0, 6],
                    'startDate': date.today().strftime('%Y-%m-%d'),
                }),
        }

    def clean_date(self):
        day = self.cleaned_data['date']

        if day <= date.today():
            raise forms.ValidationError('Date should be upcoming (tomorrow or later)', code='invalid')
        if day.isoweekday() in (0, 6):
            raise forms.ValidationError('Date should be a workday', code='invalid')

        return day'''

class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'timeslot', 'patient_name',)
        widgets = {
            'date': DateInput(),}

