from django.db import models
from complaint.models import Complaint
from django.contrib.auth.hashers import make_password
from django.contrib import admin


# Create your models here.


class AdminRole(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)

    def __str__(self):
        return self.name
class StaffProfile(models.Model): 
    id = models.AutoField(primary_key=True, serialize=False, unique=True)
    department = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, default="default_username")
    email = models.EmailField(unique=True,default="default@example.com")
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=True)
 

    def save(self, *args, **kwargs):
        if not self.pk and self.password:  # Hash password only on creation
            self.password = make_password(self.password)
        super(StaffProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.department}"
