from django.contrib import admin
from .models import User,Patient,Doctor,Service,Appointment
# Register your models here.


class AppoinmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'doctor', 'date', ]
    date_hierarchy = ('date')
    list_filter = ['date', 'doctor', ]
    list_per_page = 20
    search_fields = ['doctor', 'name', ]

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name','speciality','experience','email',]

class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','gender','age','email']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title','pricing','speciality']

class UserList(admin.ModelAdmin):
    list_display = ( 'email','username','is_active','created_on','role','is_staff','is_patient')
    list_filter = ( 'email','username','is_active','created_on','role','is_staff','is_patient')
    search_fields = ('email','username','is_active','created_on','role','is_staff','is_patient')
    ordering = ['email']

admin.site.register(Appointment,AppoinmentAdmin)
admin.site.register(User,UserList)
admin.site.register(Service)
admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Patient,PatientAdmin)
