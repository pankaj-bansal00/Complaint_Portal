import json
import traceback
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from .models import Complaint
from user.models import User
from django.http import JsonResponse
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Complaint
from user.models import User 
from django.views.decorators.csrf import csrf_exempt
import random
import string
from django.utils.timezone import now
from .utils import send_trackid
# Helper function to generate a tracking ID
def generate_tracking_id():
    """Generate a unique tracking ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def complaint_form(request):
    id = request.session.get("custid")
    
    # Ensure user is authenticated and exists
    try:
        user = get_object_or_404(User, custid=id)  # Ensure correct retrieval
    except User.DoesNotExist:
        messages.error(request, "User not found. Please log in again.")
        return redirect("user_login")  # Redirect to login if user not found

    if request.method == "POST":
        customer_type = request.POST.get("customer_type")
        bank_name = request.POST.get("bank_name")
        account_number = request.POST.get("account_number")
        complaint_type = request.POST.get("complaint_type")
        complaint_title = request.POST.get("complaint_title")
        complaint_description = request.POST.get("complaint_description")
        track_id = request.POST.get("track_id")  # Get the track_id from the form

        # Save complaint
        complaint = Complaint.objects.create(
            user=user,
            customer_type=customer_type,
            bank_name=bank_name,
            account_number=account_number,
            complaint_type=complaint_type,
            complaint_title=complaint_title,
            complaint_description=complaint_description,
            track_id=track_id  # Save the generated tracking ID
        )
        print(complaint.track_id)
        # Send SMS with the tracking ID

        send_trackid(complaint.track_id,complaint.user.phone)
        # Notify user with a success message
        messages.success(
            request, f"Your complaint has been submitted! A tracking ID has been sent to your registered phone number."
        )
        return redirect('complaint_success', track_id=complaint.track_id)  # Redirect to a success page

    return render(request, "complaint_form.html", {"user": user})



def trackid(request):  
    if request.method == "POST":
        track_id = request.POST.get("track_id")
        phone = request.POST.get("phone")  # Get phone number from input

        try:
            # Retrieve the complaint based on track_id
            complaint = Complaint.objects.get(track_id=track_id)

            # Check if the provided phone number matches the complaint's associated user
            if complaint.user.phone == phone:  # Assuming 'phone_number' exists in User model
                return render(request, "trackid.html", {"complaint": complaint})
            else:
                messages.error(request, "Phone number does not match the complaint record.")
                return redirect("trackid")

        except Complaint.DoesNotExist:
            messages.error(request, "Complaint not found.")
            return redirect("trackid")

    return render(request, 'trackid.html')

def complaint_success(request, track_id):
    return render(request, 'complaint_success.html', {'track_id': track_id})






@csrf_exempt  # If you're not using CSRF protection
def send_sms_view(request):
    if request.method == 'POST':
        return sendd_sms(request)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405) 