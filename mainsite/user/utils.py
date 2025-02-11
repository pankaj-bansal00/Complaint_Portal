from django.core.mail import send_mail
from django.conf import settings
import urllib.request
import urllib.parse
from django.http import JsonResponse
import random
import requests
import traceback
from django.utils.timezone import now
import xml.etree.ElementTree as ET
from .models import OTPVerification
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Access environment variables
APIKEY = os.getenv('APIKEY')


def generate_otp(length=7):
    """Generate a secure 6-digit OTP."""
    if length != 7:
        raise ValueError("OTP length must be 6 digits.")
    
    otp = random.randint(100000, 999999)  # Generates a 6-digit OTP
    return otp

# Example usage:
otp_code = generate_otp()
print("Generated OTP:", otp_code)


def send_otp_via_sms(request):
    try:
        # Load request data
        data = json.loads(request.body)
        phone_number = data.get('phone')
        
        if not phone_number:
            return JsonResponse({'success': False, 'error': 'Phone number is required'}, status=400)

        # Generate OTP
        otp = generate_otp()
        
        # Vonage (or custom SMS provider) API credentials
        userid = os.getenv('USERID')
        sender = os.getenv('SENDER')
        api_key = os.getenv('API_KEY')
        template_id = os.getenv("TEMPLATE_ID")

        # Message to send
        message_body = (f"Dear Customer, your Customer Complaint Form OTP is {otp}. "
                         "This OTP is valid for 3 minutes. Do not share OTP with anyone "
                         "for security reasons. Thanks, The Sirsa Central Cooperative Bank Limited.")
        
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
        otp_record, created = OTPVerification.objects.get_or_create(phone=phone_number)
        otp_record.otp = otp
        otp_record.created_at = now()
        otp_record.save()

        if created:
            print("New OTP record created.")
        else:
            print("OTP record updated.")

        # Make the API request
        response = requests.post(url, data=payload)

        # Handle the API response
        if response.status_code == 200:
            print(f"OTP sent to {phone_number}. OTP: {otp}")
            return JsonResponse({'success': True, 'message': 'OTP sent successfully.'})
        else:
            print(f"Failed to send OTP. HTTP Status: {response.status_code}")
            return JsonResponse({'success': False, 'error': f"HTTP Error {response.status_code}"}, status=500)
    
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=500)