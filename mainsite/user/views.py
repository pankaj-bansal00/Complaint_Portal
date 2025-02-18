from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login
import random
from .models import User, OTPVerification
from .utils import send_otp_via_sms

def user_register(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        otp = request.POST.get("otp")
        name = request.POST.get("name")
        email = request.POST.get("email")

        # Debugging logs
        print("Phone:", phone, "OTP:", otp)

        # Check if OTP entry exists
        user_otp = OTPVerification.objects.filter(phone=phone).first()
        print("OTP Record:", user_otp)

        if not user_otp:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'verify_otp.html', {'phone': phone})

        # Check OTP expiration (3-minute window)
        if timezone.now() - user_otp.created_at > timezone.timedelta(minutes=3):
            messages.error(request, 'OTP has expired. Please request a new one.')
            return render(request, 'verify_otp.html', {'phone': phone})

        # Validate OTP and register user
        if otp == user_otp.otp:
            user, created = User.objects.get_or_create(phone=phone, defaults={'name': name, 'email': email})
            request.session["custid"] = user.pk  # Use the primary key if custid is not defined
            messages.success(request, 'User registered successfully.')
            return redirect('complaint_form')
        
        messages.error(request, 'Incorrect OTP. Please try again.') 
        return render(request, 'user_register.html')

    return render(request, 'user_register.html')



def user_login(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        phone = request.POST.get('phone')
        if not User.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number not registered.')
            return redirect('user_register')
            print("Phone:", phone,)

        # Check if OTP entry exists
        user_otp = OTPVerification.objects.filter(phone=phone).first()
        print("OTP Record:", user_otp)

        if not user_otp:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'verify_otp.html', {'phone': phone})

        # Check OTP expiration (3-minute window)
        if timezone.now() - user_otp.created_at > timezone.timedelta(minutes=3):
            messages.error(request, 'OTP has expired. Please request a new one.')
            return render(request, 'verify_otp.html', {'phone': phone})

       # Validate OTP and register user
        if otp == user_otp.otp:
            user, created = User.objects.get_or_create(phone=phone)
            request.session["custid"] = user.pk  # Use the primary key if custid is not defined
            messages.success(request, 'User registered successfully.')
            return redirect('complaint_form')
        
        messages.error(request, 'Incorrect OTP. Please try again.') 
        return render(request, 'user_register.html')
    return render(request, 'user_login.html')

def verify_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        try:
            user_otp = OTPVerification.objects.get(phone=phone, otp=otp)
            print("user_otp",user_otp)
            print("otp",otp)
            if user_otp.is_expired():
                messages.error(request, 'OTP expired. Request a new one.')
                return render(request, 'verify_otp.html', {'phone': phone})

            user = User.objects.get(phone=phone)
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('complaintform')  # Adjust redirect

        except OTPVerification.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'verify_otp.html', {'phone': phone})

    return redirect('user_login')

def resend_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if not User.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number not registered.')
            return redirect('user_register')

        otp = str(random.randint(100000, 999999))
        OTPVerification.objects.create(phone=phone, otp=otp)
        send_otp_via_sms(phone, otp)
        messages.success(request, 'A new OTP has been sent to your phone.')
        return render(request, 'verify_otp.html', {'phone': phone})

    return redirect('user_login')



def home(request):
    # Check if the user is logged in with a session
    if request.session.get("custid"):
        id = request.session.get("custid")
        try:
            user = User.objects.get(custid=id)  # Get single user object
            return render(request, 'home.html', {"user": user})
        except User.DoesNotExist:
            return redirect('user_login')  # Handle missing user gracefully
    return render(request, 'home.html')

def logout(request):
    # Clear all session data
    request.session.flush()
    # Redirect to the home page after logout
    return redirect('user_register')

