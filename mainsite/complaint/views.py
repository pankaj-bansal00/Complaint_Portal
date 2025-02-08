from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Complaint
from django.contrib.auth.decorators import login_required
from user.models import User


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Complaint
from user.models import User  # Ensure correct import

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

        # Ensure 'user' is a valid User instance
        if not isinstance(user, User):
            messages.error(request, "Invalid user. Please log in again.")
            return redirect("user_login")

        # Save complaint
        print("user",user,type(user))
        complaint = Complaint.objects.create(
            user=user,
            customer_type=customer_type,
            bank_name=bank_name,
            account_number=account_number,
            complaint_type=complaint_type,
            complaint_title=complaint_title,
            complaint_description=complaint_description
        )

        messages.success(request, f"Complaint submitted successfully! Your Track ID: {complaint.track_id}")
        return redirect("trackid")

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