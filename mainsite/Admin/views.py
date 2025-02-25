from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Complaint
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Complaint
from .models import StaffProfile
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import now, timedelta  # Import 'now' correctly


# Restrict access to admin users only
def is_admin(user):
    return user.is_staff and user.is_superuser

def admin_dashboard(request): 
    today = now().date()
    yesterday = today - timedelta(days=1)

    # Complaints created today & yesterday
    today_complaints = Complaint.objects.filter(created_at__date=today).count()
    yesterday_complaints = Complaint.objects.filter(created_at__date=yesterday).count()

    # Complaints resolved today & yesterday
    today_resolved_complaints = Complaint.objects.filter(status='resolved', resolved_at__date=today).count()
    yesterday_resolved_complaints = Complaint.objects.filter(status='resolved', resolved_at__date=yesterday).count()

    # Other complaint counts
    pending_count = Complaint.objects.filter(status='pending').count()
    under_process_count = Complaint.objects.filter(status='Under Process').count()
    resolved_count = Complaint.objects.filter(status='resolved').count()
    total_count = Complaint.objects.count()

    # Pass data to the template
    context = {
        'pending_count': pending_count,
        'under_process_count': under_process_count,
        'resolved_count': resolved_count,
        'total_count': total_count,
        'today_complaints': today_complaints,
        'yesterday_complaints': yesterday_complaints,
        'today_resolved_complaints': today_resolved_complaints,
        'yesterday_resolved_complaints': yesterday_resolved_complaints,
    }
    return render(request, "admin_dashboard.html", context)

def admin_login(request):
    if request.user.is_superuser :
        return redirect('admin_dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not authorized.")

    return render(request, "admin_login.html")

def logout_view(request):
    if request.user.is_superuser:
        logout(request)
        return redirect('admin_login')
    else:
        return redirect('staff_login')  


# Staff register and login

def staff_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # ✅ Check if username already exists
        if StaffProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('staff_register')

        # ✅ Check if email already exists
        if StaffProfile.objects.filter(email=email).exists():
            messages.error(request, "Email already in use. Please use a different one.")
            return redirect('staff_register')

        if password == confirm_password:
            staff = StaffProfile.objects.create(username=username, email=email, password=make_password(password))
            messages.success(request, "Staff registered successfully.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, "staff_register.html")

def staff_login(request):
  if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Attempting login for:", username)

        try:
            # Get the staff member with the provided username
            staff = StaffProfile.objects.get(username=username)
            print("staff",staff)
            print("password",staff.password)
            if check_password(password, staff.password):  # Verify password
                request.session["id"] = (
                    staff.id
                ) 
                
                 # Store staff_id in the session
                messages.success(request, "Logged in successfully!")
                print("Login successful, redirecting to dashboard...")
                return redirect("complaint_dashboard")  # Redirect to seller dashboard
            else:
                print("Invalid credentials: Password mismatch")
                messages.error(request, "Invalid credentials    . Please try again.")
                return redirect("staff_login")
        except StaffProfile.DoesNotExist:
            print("Seller with username not found:", username)
            messages.error(request, "No staff account found with this username.")
            return redirect("staff_login")

  return render(request, "staff_login.html")

@csrf_exempt
def change_password(request, staff_id):
    """ Change the password of a staff member """
    if request.method == "POST":
        data = json.loads(request.body)
        new_password = data.get("password")

        staff = get_object_or_404(StaffProfile, id=staff_id)
        staff.password = make_password(new_password)  # ✅ Hashing password
        staff.save()

        return JsonResponse({"message": "Password updated successfully."})
    return JsonResponse({"error": "Invalid request"}, status=400)
@csrf_exempt
def change_email(request, staff_id):
    """ Change the email of a staff member """
    if request.method == "POST":
        data = json.loads(request.body)
        new_email = data.get("email")
        
        staff = get_object_or_404(StaffProfile, id=staff_id)  # ✅ Fixed here
        staff.email = new_email
        staff.save()
        
        return JsonResponse({"message": "Email updated successfully."})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def delete_staff(request, staff_id):
    """ Delete a staff member """
    if request.method == "DELETE":
        staff = get_object_or_404(StaffProfile, id=staff_id)
        staff.delete()
        return JsonResponse({"message": "Staff deleted successfully."})
    return JsonResponse({"error": "Invalid request"}, status=400)

def staff_list(request):
    """ Fetch and display all staff members """
    staff_members = StaffProfile.objects.all()
    return render(request, "staff_list.html", {"staff_list": staff_members})



# Complaint Dashboard in which complaints are displayed according to the filter
def complaint_dashboard(request):
    today = now().date()
    yesterday = today - timedelta(days=1)

    # Complaints created today & yesterday
    today_complaints = Complaint.objects.filter(created_at__date=today).count()
    yesterday_complaints = Complaint.objects.filter(created_at__date=yesterday).count()

    # Complaints resolved today & yesterday
    today_resolved_complaints = Complaint.objects.filter(status='resolved', resolved_at__date=today).count()
    yesterday_resolved_complaints = Complaint.objects.filter(status='resolved', resolved_at__date=yesterday).count()

    # Other complaint counts
    pending_count = Complaint.objects.filter(status='pending').count()
    under_process_count = Complaint.objects.filter(status='Under Process').count()
    resolved_count = Complaint.objects.filter(status='resolved').count()
    total_count = Complaint.objects.count()

    # Pass data to the template
    context = {
        'pending_count': pending_count,
        'under_process_count': under_process_count,
        'resolved_count': resolved_count,
        'total_count': total_count,
        'today_complaints': today_complaints,
        'yesterday_complaints': yesterday_complaints,
        'today_resolved_complaints': today_resolved_complaints,
        'yesterday_resolved_complaints': yesterday_resolved_complaints,
    }

    return render(request, 'complaints/complaint_dashboard.html', context)




def complaint_list(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'complaints/total_complaints.html', {'complaints': complaints})

# Admin Dashboard - Complaint Details
@user_passes_test(is_admin)
def admin_complaint_detail(request, track_id):
    complaint = get_object_or_404(Complaint, track_id=track_id)
    return render(request, "complaints/admin_complaint_detail.html", {"complaint": complaint})

# Admin Dashboard - Update Complaint Status
@user_passes_test(is_admin)
def update_complaint_status(request, track_id):
    complaint = get_object_or_404(Complaint, track_id=track_id)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        response_message = request.POST.get("response_message")
        complaint.status = new_status
        complaint.save()

        # Send email or notification to user (if needed)
        # You can integrate Django's email system here.

        return redirect('admin_complaint_detail', track_id=track_id)

    return render(request, 'complaints/update_complaint_status.html', {'complaint': complaint})

# Admin Dashboard - Delete Complaint
@user_passes_test(is_admin)
def delete_complaint(request, track_id):
    complaint = get_object_or_404(Complaint, track_id=track_id)
    complaint.delete()
    return redirect('total_complaints')

@user_passes_test(is_admin)
def resolve_complaint(request, track_id):
    complaint = get_object_or_404(Complaint, track_id=track_id)
    complaint.status = "resolved"
    complaint.save()
    return redirect('complaints/admin_complaint_detail', track_id=track_id)

@user_passes_test(is_admin)
def close_complaint(request, track_id):
    complaint = get_object_or_404(Complaint, track_id=track_id)    
    complaint.status = "closed"
    complaint.save()
    return redirect('complaints/admin_complaint_detail', track_id=track_id)


def pending_complaints(request):
    pending_complaints = Complaint.objects.filter(status='pending').order_by('-created_at')

    context = {
        'pending_complaints': pending_complaints
    }
    return render(request, 'complaints/pending_complaint.html', context)


def under_process_complaints(request):
    under_process_complaints = Complaint.objects.filter(status='Under Process').order_by('-created_at')

    context = {
        'under_process_complaints': under_process_complaints
    }
    return render(request, 'complaints/underprocess.html', context)


def resolved_complaints(request):
    resolved_complaints = Complaint.objects.filter(status='resolved').order_by('-resolved_at')

    context = {
        'resolved_complaints': resolved_complaints
    }
    return render(request, 'complaints/resolved.html', context)


def today_complaints(request):
    today = now().date()
    complaints = Complaint.objects.filter(created_at__date=today).order_by('-created_at')

    context = {
        'complaints': complaints,
        'today_complaints_count': complaints.count(),
    }
    return render(request, 'complaints/today_complaints.html', context)

def today_resolved_complaints(request):
    today = now().date()
    resolved_complaints = Complaint.objects.filter(status='resolved', resolved_at__date=today).order_by('-resolved_at')

    context = {
        'resolved_complaints': resolved_complaints,
        'today_resolved_count': resolved_complaints.count(),
    }
    return render(request, 'complaints/today_resolved_complaints.html', context)