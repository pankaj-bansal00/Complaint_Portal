from django.contrib import admin
from .models import Complaint


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('track_id', 'user', 'customer_type', 'bank_name', 'complaint_type', 'status', 'created_at')
    list_filter = ('status', 'bank_name', 'complaint_type', 'created_at')
    search_fields = ('track_id', 'user__username', 'complaint_title', 'complaint_description')
    ordering = ('-created_at',)

    # Allow admin to update the status
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ['track_id', 'user', 'customer_type', 'bank_name', 'account_number', 'complaint_type', 'complaint_title', 'complaint_description', 'created_at']
        return []

# Correct way to register
admin.site.register(Complaint, ComplaintAdmin)

