from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff_register/', views.staff_register, name='staff_register'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('logout/', views.logout_view, name='logout'),
    path("staff_list/", views.staff_list, name="staff_list"),

    path("change_password/<int:staff_id>/", views.change_password, name="change_password"),
    path("change_email/<int:staff_id>/", views.change_email, name="change_email"),
    path("delete_staff/<int:staff_id>/", views.delete_staff, name="delete_staff"),

    path('complaints/', views.complaint_list, name='admin_complaint_list'),
    path('complaints/<str:track_id>/', views.admin_complaint_detail, name='admin_complaint_detail'),
    path('complaints/<str:track_id>/update/', views.update_complaint_status, name='update_complaint_status'),
    path('complaints/<str:track_id>/delete/', views.delete_complaint, name='delete_complaint'),
    path('complaints/<str:track_id>/resolve/', views.resolve_complaint, name='resolve_complaint'),
    path('complaints/<str:track_id>/close/', views.close_complaint, name='close_complaint'),
    path('complaint_dashboard/', views.complaint_dashboard, name='complaint_dashboard'),
]
