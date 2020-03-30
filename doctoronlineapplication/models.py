from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, UserManager
from .utils import ROLES
# Create your models here.



class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    role = models.CharField(choices=ROLES, max_length=50)
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name if full_name else self.email

    @property
    def full_name(self):
        return self.get_full_name()



class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()


    def __str__(self):
        return self.title


class Doctor(models.Model):
    name = models.CharField(max_length=120)
    speciality = models.CharField(max_length=120)
    details = models.TextField()
    experience = models.TextField()
    twitter = models.CharField(max_length=120, blank=True, null=True)
    facebook = models.CharField(max_length=120, blank=True, null=True)
    instagram = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.name



class Appointment(models.Model):
    time_choices = (
            (0, '09:00 – 10:00'),
            (1, '10:00 – 11:00'),
            (2, '11:00 – 12:00'),
            (3, '12:00 – 13:00'),
            (4, '13:00 – 14:00'),
            (5, '14:00 – 15:00'),
            (6, '15:00 – 16:00'),
            (7, '16:00 – 17:00'),
            (8, '17:00 – 18:00'),
         )

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField(default=timezone.now)
    time = models.IntegerField(choices=time_choices)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.doctor.name}"


class Patient(models.Model):

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=256, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'),
                                                       ('prefer not to say', 'Prefer Not To Say')],
                              default='Select a gender', blank=False)
    age = models.IntegerField(default = 18, blank=False)
    address = models.CharField(max_length=120)
    previous_medications =  models.CharField(max_length=120)
    dateofbirth = models.DateTimeField(max_length=120)
    date_created = models.CharField(null=True,max_length=20)

    def __str__(self):
        return self.first_name
