from django.urls import path
from . import views

urlpatterns = [
    path('trackid/', views.trackid, name='trackid'),
    path('complaint_form/', views.complaint_form, name='complaint_form'),
    path('complaint_success/<str:track_id>/', views.complaint_success, name='complaint_success'),
    
]