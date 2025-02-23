from django.shortcuts import render, redirect
from django.http import HttpResponse
from user.models import User
from user import views

# Create your views here.=
def demo_home(request):
    return render(request,'home1.html')