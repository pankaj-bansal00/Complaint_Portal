from django.db import models
from django.contrib.auth import get_user_model
from user.models import User
import random
from django.utils.timezone import now


def generate_trackid():
    existing_trackids = set(Complaint.objects.values_list("track_id", flat=True))  # Fetch all existing track IDs

    while True:
        random_number = random.randint(10000, 99999)  # Generate a 5-digit random number
        trackid = f"SIRSAB{random_number}"  # Format: SIRSAB12345

        if trackid not in existing_trackids:  # Ensure uniqueness
            return trackid

class Complaint(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('existing', 'Existing Customer'),
        ('new', 'New Customer'),
    ]


    COMPLAINT_TYPE_CHOICES = [
        ('transaction', 'Transaction Issue'),
        ('account', 'Account Problem'),
        ('service', 'Service Complaint'),
        ('fraud', 'Fraud Report'),
        ('other', 'Other'),
    ]


    track_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES)
    account_number = models.CharField(max_length=16)
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPE_CHOICES)
    complaint_title = models.CharField(max_length=200)
    complaint_description = models.TextField(max_length=500)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'),('Under Process', 'Under Process'),('resolved', 'Resolved')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

 
    def save(self, *args, **kwargs):
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = now()  # Automatically set resolution time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.complaint_title} ({self.track_id})"

    def save(self, *args, **kwargs):
        if not self.track_id:
            self.track_id = generate_trackid()
        super().save(*args, **kwargs)