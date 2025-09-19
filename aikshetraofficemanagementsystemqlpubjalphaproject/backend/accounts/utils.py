"""
Utility functions for user management and authentication.
"""

import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def generate_employee_id(department=None):
    """
    Generate unique employee ID based on department and random number.
    """
    
    # Department prefix mapping
    dept_prefixes = {
        'Engineering': 'ENG',
        'Marketing': 'MKT',
        'Sales': 'SAL',
        'HR': 'HR',
        'Finance': 'FIN',
        'Operations': 'OPS',
        'IT': 'IT',
    }
    
    # Get department prefix or use default
    prefix = dept_prefixes.get(department, 'EMP')
    
    # Generate random 4-digit number
    random_num = ''.join(random.choices(string.digits, k=4))
    
    return f"{prefix}{random_num}"


def send_welcome_email(user):
    """
    Send welcome email to newly registered user.
    """
    
    subject = 'Welcome to Office Management System'
    
    # Prepare email context
    context = {
        'user': user,
        'company_name': 'Your Company',
        'login_url': f"{settings.FRONTEND_URL}/login" if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:3000/login',
    }
    
    # Render email templates
    html_message = render_to_string('emails/welcome.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send welcome email to {user.email}: {str(e)}")
        return False


def send_approval_notification(user, approved_by):
    """
    Send email notification when user is approved.
    """
    
    subject = 'Account Approved - Office Management System'
    
    context = {
        'user': user,
        'approved_by': approved_by,
        'login_url': f"{settings.FRONTEND_URL}/login" if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:3000/login',
    }
    
    html_message = render_to_string('emails/approval.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send approval email to {user.email}: {str(e)}")
        return False


def send_admin_notification_new_user(user):
    """
    Notify admins about new user registration requiring approval.
    """
    
    from .models import User
    
    # Get all admin users
    admin_users = User.objects.filter(role='admin', is_active=True)
    admin_emails = [admin.email for admin in admin_users]
    
    if not admin_emails:
        return False
    
    subject = 'New User Registration Requires Approval'
    
    context = {
        'user': user,
        'admin_url': f"{settings.FRONTEND_URL}/admin/approvals" if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:3000/admin/approvals',
    }
    
    html_message = render_to_string('emails/admin_new_user.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send admin notification: {str(e)}")
        return False


def validate_file_upload(file, allowed_types=None, max_size_mb=5):
    """
    Validate uploaded files for type and size.
    """
    
    if allowed_types is None:
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
    
    # Check file type
    if file.content_type not in allowed_types:
        return False, f"File type {file.content_type} not allowed"
    
    # Check file size (convert MB to bytes)
    max_size_bytes = max_size_mb * 1024 * 1024
    if file.size > max_size_bytes:
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    return True, "File is valid"


def get_user_permissions(user):
    """
    Get user permissions based on role.
    """
    
    base_permissions = [
        'view_profile',
        'edit_profile',
        'view_tasks',
        'view_attendance',
    ]
    
    role_permissions = {
        'admin': [
            'manage_users',
            'approve_users',
            'manage_departments',
            'manage_projects',
            'manage_tasks',
            'view_all_attendance',
            'manage_payroll',
            'manage_courses',
            'view_reports',
            'manage_announcements',
        ],
        'employee': [
            'create_tasks',
            'manage_own_tasks',
            'mark_attendance',
            'request_leave',
            'view_salary',
            'enroll_courses',
        ],
        'trainee': [
            'mark_attendance',
            'request_leave',
            'enroll_courses',
            'view_learning_materials',
        ],
    }
    
    permissions = base_permissions.copy()
    permissions.extend(role_permissions.get(user.role, []))
    
    return permissions
