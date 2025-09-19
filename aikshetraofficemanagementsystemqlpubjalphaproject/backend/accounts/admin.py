"""
Django admin configuration for user management.
Provides comprehensive user administration interface.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Enhanced user admin with role-based management and approval workflow.
    """
    
    list_display = [
        'email', 'get_full_name', 'role', 'is_approved', 
        'department', 'hire_date', 'is_active', 'date_joined'
    ]
    list_filter = ['role', 'is_approved', 'is_active', 'department', 'hire_date']
    search_fields = ['email', 'first_name', 'last_name', 'employee_id']
    ordering = ['-date_joined']
    
    # Custom fieldsets for the admin form
    fieldsets = (
        ('Authentication', {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone', 'date_of_birth', 'address', 'profile_picture', 'bio')
        }),
        ('Employment Details', {
            'fields': ('role', 'employee_id', 'department', 'position', 'hire_date', 'salary')
        }),
        ('Approval Status', {
            'fields': ('is_approved', 'approved_by', 'approved_at'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['approved_at', 'date_joined', 'last_login']
    
    def get_full_name(self, obj):
        """Display full name in admin list"""
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('approved_by')
    
    actions = ['approve_users', 'disapprove_users']
    
    def approve_users(self, request, queryset):
        """Bulk approve selected users"""
        updated = 0
        for user in queryset.filter(is_approved=False):
            user.approve_user(request.user)
            updated += 1
        
        self.message_user(
            request,
            f'{updated} user(s) were successfully approved.'
        )
    approve_users.short_description = "Approve selected users"
    
    def disapprove_users(self, request, queryset):
        """Bulk disapprove selected users"""
        updated = queryset.update(is_approved=False, approved_by=None, approved_at=None)
        self.message_user(
            request,
            f'{updated} user(s) were disapproved.'
        )
    disapprove_users.short_description = "Disapprove selected users"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for extended user profiles.
    """
    
    list_display = ['user', 'emergency_contact_name', 'theme_preference', 'updated_at']
    list_filter = ['theme_preference', 'updated_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'emergency_contact_name']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')
        }),
        ('Professional Information', {
            'fields': ('skills', 'certifications')
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'github_url')
        }),
        ('Preferences', {
            'fields': ('theme_preference', 'notification_preferences')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user')


# Customize admin site headers
admin.site.site_header = "Office Management System"
admin.site.site_title = "Office Management Admin"
admin.site.index_title = "Welcome to Office Management Administration"
