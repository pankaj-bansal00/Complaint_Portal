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
from user.models import User  # Ensure correct import

import random
import string
from django.utils.timezone import now
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

        # Send SMS with the tracking ID
        track_id_message = (
            f"Dear {user.name}, your complaint has been successfully registered. "
            f"Your Tracking ID is {track_id}. You can use this ID to track your complaint."
        )
        sendd_sms(track_id_message)

        # Notify user with a success message
        messages.success(
            request, f"Your complaint has been submitted! A tracking ID has been sent to your registered phone number."
        )
        return redirect('complaint_success')  # Redirect to a success page

    return render(request, "complaint_form.html", {"user": user})


def trackid(request):  
    if request.method == "POST":
        print("trackid33333333")
        track_id = request.POST.get("track_id")
        try:
            
            complaint = Complaint.objects.get(track_id=track_id)
            print("complaint",complaint)
            return render(request, "trackid.html", {"complaint": complaint})
        except Complaint.DoesNotExist:
            messages.error(request, "Complaint not found.")
            return redirect("trackid")
    return render(request, 'trackid.html')

def complaint_success(request):
    return render(request, 'complaint_success.html')

def sendd_sms(request):
    try:
        # Load request data
        data = json.loads(request.body)
        phone_number = data.get('phone')
        
        if not phone_number:
            return JsonResponse({'success': False, 'error': 'Phone number is required'}, status=400)

        # Generate trackid
        trackkid = generate_tracking_id()
        trackid = trackkid

        # Vonage (or custom SMS provider) API credentials
        userid = os.getenv('USERID')
        sender = os.getenv('SENDER')
        api_key = os.getenv('API_KEY')
        template_id = os.getenv("TEMPLATE_ID")

        # Message to send
        message_body = (f"""Dear Customer, your Customer Complaint Form Tracking ID is {trackid}. "
                         "This Tracking ID. Do not share Tracking ID with anyone "
                         "for security reasons. "
                         "Thanks, The Sirsa Central Cooperative Bank Limited.""")
        
        # API URL
        url = 'https://www.proactivesms.in/sendsms.jsp'

        # Payload for the API request
        payload = {
            'user': userid,
            'password': api_key,
            'senderid': sender,
            'mobiles': phone_number,
            'sms': message_body,
            'tempid': template_id
        }

        # Create or update OTP record
        trackid, created = Complaint.objects.get_or_create(phone=phone_number)
        if created:
            print("New Trackid  record created.")
        else:
            print("Trackid record updated.")

        # Make the API request
        response = requests.post(url, data=payload)

        # Handle the API response
        if response.status_code == 200:
            print(f"OTP sent to {phone_number}. OTP: {trackid}")
            return JsonResponse({'success': True, 'message': 'OTP sent successfully.'})
        else:
            print(f"Failed to send OTP. HTTP Status: {response.status_code}")
            return JsonResponse({'success': False, 'error': f"HTTP Error {response.status_code}"}, status=500)
    
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
