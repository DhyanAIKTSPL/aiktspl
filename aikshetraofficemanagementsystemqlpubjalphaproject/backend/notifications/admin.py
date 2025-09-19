"""
Django admin for notification management.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Notification, NotificationPreference, SystemAnnouncement


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'recipient', 'notification_type', 'is_read', 
        'is_sent', 'created_at'
    ]
    list_filter = ['notification_type', 'is_read', 'is_sent', 'created_at']
    search_fields = ['title', 'message', 'recipient__first_name', 'recipient__last_name']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('recipient', 'title', 'message', 'notification_type')
        }),
        ('Actions', {
            'fields': ('action_url', 'action_label')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at', 'is_sent', 'sent_at')
        }),
        ('Metadata', {
            'fields': ('data',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['read_at', 'sent_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient')


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_enabled', 'push_enabled', 'inapp_enabled', 'quiet_hours_enabled']
    list_filter = ['email_enabled', 'push_enabled', 'inapp_enabled', 'quiet_hours_enabled']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Email Notifications', {
            'fields': (
                'email_enabled', 'email_task_updates', 'email_attendance_reminders',
                'email_salary_updates', 'email_learning_updates', 'email_system_updates'
            )
        }),
        ('Push Notifications', {
            'fields': (
                'push_enabled', 'push_task_updates', 'push_attendance_reminders',
                'push_salary_updates', 'push_learning_updates', 'push_system_updates'
            )
        }),
        ('In-App Notifications', {
            'fields': (
                'inapp_enabled', 'inapp_task_updates', 'inapp_attendance_reminders',
                'inapp_salary_updates', 'inapp_learning_updates', 'inapp_system_updates'
            )
        }),
        ('Quiet Hours', {
            'fields': ('quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end')
        }),
    )


@admin.register(SystemAnnouncement)
class SystemAnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'priority', 'is_published', 'is_active', 
        'publish_at', 'expire_at', 'created_by'
    ]
    list_filter = ['priority', 'is_published', 'is_active', 'publish_at']
    search_fields = ['title', 'content']
    
    fieldsets = (
        ('Announcement Details', {
            'fields': ('title', 'content', 'priority')
        }),
        ('Targeting', {
            'fields': ('target_roles', 'target_departments')
        }),
        ('Scheduling', {
            'fields': ('publish_at', 'expire_at')
        }),
        ('Status', {
            'fields': ('is_active', 'is_published', 'created_by')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')
