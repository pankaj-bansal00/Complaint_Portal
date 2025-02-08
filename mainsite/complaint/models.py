from django.db import models
from django.contrib.auth import get_user_model
import uuid
from user.models import User



class Complaint(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('existing', 'Existing Customer'),
        ('new', 'New Customer'),
    ]

    BANK_CHOICES = [
        ('hdfc', 'HDFC Bank'),
        ('sbi', 'State Bank of India'),
        ('icici', 'ICICI Bank'),
        ('axis', 'Axis Bank'),
        ('pnb', 'Punjab National Bank'),
    ]

    COMPLAINT_TYPE_CHOICES = [
        ('transaction', 'Transaction Issue'),
        ('account', 'Account Problem'),
        ('service', 'Service Complaint'),
        ('fraud', 'Fraud Report'),
        ('other', 'Other'),
    ]

    TRACK_ID_PREFIX = "CMP"

    track_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES)
    bank_name = models.CharField(max_length=50, choices=BANK_CHOICES)
    account_number = models.CharField(max_length=20)
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPE_CHOICES)
    complaint_title = models.CharField(max_length=200)
    complaint_description = models.TextField(max_length=500)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Generate a unique Track ID for each complaint """
        if not self.track_id:
            self.track_id = f"{self.TRACK_ID_PREFIX}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.track_id} - {self.complaint_title}"
