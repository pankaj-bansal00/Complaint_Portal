from django.urls import path
from . import views
from user import views as user_views
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [
    path('staff_login/', views.staff_login, name='staff_login'),
    path('logout/', views.logout_view, name='logout'),
    path('complaints/', views.complaint_list, name='admin_complaint_list'),
    path('complaints/<str:track_id>/', views.admin_complaint_detail, name='admin_complaint_detail'),
    path('complaints/<str:track_id>/update/', views.update_complaint_status, name='update_complaint_status'),
    path('complaints/<str:track_id>/delete/', views.delete_complaint, name='delete_complaint'),
    path('complaints/<str:track_id>/resolve/', views.resolve_complaint, name='resolve_complaint'),
    path('complaints/<str:track_id>/close/', views.close_complaint, name='close_complaint'),
    path('adminmain/', views.adminmain, name='adminmain'),
]
