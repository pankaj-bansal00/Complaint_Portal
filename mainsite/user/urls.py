from django.urls import path
from . import views
from .utils import send_otp_via_sms


urlpatterns = [
    path('user_register/', views.user_register, name='user_register'),
    path('user_login/', views.user_login, name='user_login'),
    path('resend-otp/', views.resend_otp, name='resend_otp'), 
    path("send-otp/", send_otp_via_sms, name="send_otp"),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout, name='logout'),
]