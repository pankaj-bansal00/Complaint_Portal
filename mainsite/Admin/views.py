from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Complaint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Complaint

def adminmain(request):
    pending_count = Complaint.objects.filter(status='pending').count()
    under_process_count = Complaint.objects.filter(status='Under Process').count()
    resolved_count = Complaint.objects.filter(status='resolved').count()
    total_count = Complaint.objects.count()

    context = {
        'pending_count': pending_count,
        'under_process_count': under_process_count,
        'resolved_count': resolved_count,
        'total_count': total_count
    }
    
    return render(request, 'adminmain.html', context)

# Restrict access to admin users only
def is_admin(user):
    return user.is_staff or user.is_superuser

def staff_login(request):
    if request.user.is_superuser and request.user.is_staff:
        return redirect('adminmain')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_complaint_list')
        else:
            messages.error(request, "Invalid credentials or not authorized.")

    return render(request, "staff_login.html")

def logout_view(request):
    logout(request)
    return redirect('staff_login')

# Admin Dashboard - List Complaints
@user_passes_test(is_admin)
def complaint_list(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'admin_complaint_list.html', {'complaints': complaints})

# Admin Dashboard - Complaint Details
@user_passes_test(is_admin)
def admin_complaint_detail(request, track_id):
    complaint = get_object_or_404(Complaint, track_id=track_id)
    return render(request, "admin_complaint_detail.html", {"complaint": complaint})

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

    return render(request, 'update_complaint_status.html', {'complaint': complaint})

# Admin Dashboard - Delete Complaint
@user_passes_test(is_admin)
def delete_complaint(request, track_id):
    complaint = get_object_or_404(Complaint, track_id=track_id)
    complaint.delete()
    return redirect('admin_complaints')

@user_passes_test(is_admin)
def resolve_complaint(request, track_id):
    complaint = get_object_or_404(Complaint, track_id=track_id)
    complaint.status = "resolved"
    complaint.save()
    return redirect('admin_complaint_detail', track_id=track_id)

@user_passes_test(is_admin)
def close_complaint(request, track_id):
    complaint = get_object_or_404(Complaint, track_id=track_id)    
    complaint.status = "closed"
    complaint.save()
    return redirect('admin_complaint_detail', track_id=track_id)
