"""
Django admin for attendance management.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import AttendanceRecord, LeaveRequest


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'date', 'status', 'check_in_time', 'check_out_time', 
        'hours_worked', 'overtime_hours'
    ]
    list_filter = ['status', 'date', 'user__department']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Employee & Date', {
            'fields': ('user', 'date', 'status')
        }),
        ('Time Tracking', {
            'fields': ('check_in_time', 'check_out_time', 'hours_worked', 'overtime_hours')
        }),
        ('Location', {
            'fields': ('check_in_location', 'check_out_location'),
            'classes': ('collapse',)
        }),
        ('Notes & Approval', {
            'fields': ('notes', 'approved_by'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'approved_by')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'leave_type', 'start_date', 'end_date', 
        'duration_days', 'status', 'approved_by'
    ]
    list_filter = ['leave_type', 'status', 'start_date', 'user__department']
    search_fields = ['user__first_name', 'user__last_name', 'reason']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Leave Details', {
            'fields': ('user', 'leave_type', 'start_date', 'end_date', 'reason')
        }),
        ('Status & Approval', {
            'fields': ('status', 'approved_by', 'approved_at', 'rejection_reason')
        }),
        ('Supporting Documents', {
            'fields': ('supporting_document',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['approved_at']
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        updated = 0
        for leave_request in queryset.filter(status='pending'):
            leave_request.approve(request.user)
            updated += 1
        
        self.message_user(request, f'{updated} leave request(s) approved.')
    approve_requests.short_description = "Approve selected leave requests"
    
    def reject_requests(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='rejected',
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, f'{updated} leave request(s) rejected.')
    reject_requests.short_description = "Reject selected leave requests"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'approved_by')
