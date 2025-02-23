from django.contrib import admin
from .models import Complaint, AdminRole, StaffProfile

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('track_id', 'user', 'customer_type', 'bank_name', 'complaint_type', 'status', 'created_at')
    list_filter = ('status', 'bank_name', 'complaint_type', 'created_at')
    search_fields = ('track_id', 'user__username', 'complaint_title', 'complaint_description')
    ordering = ('-created_at',)

admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(AdminRole)
admin.site.register(StaffProfile)
