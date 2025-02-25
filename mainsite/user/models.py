from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here
class User(models.Model):
    custid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10, unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"OTP for {self.email}"


class OTPVerification(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.phone} - {self.otp}"
    