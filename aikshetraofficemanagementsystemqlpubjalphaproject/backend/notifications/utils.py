"""
Utility functions for notification management.
"""

from .models import Notification, NotificationPreference
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

User = get_user_model()


def create_notification(recipient, title, message, notification_type='info', 
                       action_url='', action_label='', data=None):
    """
    Create a new notification for a user.
    """
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url,
        action_label=action_label,
        data=data or {}
    )


def create_bulk_notifications(recipients, title, message, notification_type='info',
                            action_url='', action_label='', data=None):
    """
    Create notifications for multiple users.
    """
    notifications = []
    for recipient in recipients:
        notifications.append(
            Notification(
                recipient=recipient,
                title=title,
                message=message,
                notification_type=notification_type,
                action_url=action_url,
                action_label=action_label,
                data=data or {}
            )
        )
    
    return Notification.objects.bulk_create(notifications)


def notify_admins(title, message, notification_type='system', action_url='', action_label=''):
    """
    Send notification to all admin users.
    """
    admin_users = User.objects.filter(role='admin', is_active=True)
    return create_bulk_notifications(
        recipients=admin_users,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url,
        action_label=action_label
    )


def notify_department(department_name, title, message, notification_type='info',
                     action_url='', action_label='', exclude_user=None):
    """
    Send notification to all users in a department.
    """
    users = User.objects.filter(
        department=department_name,
        is_active=True,
        is_approved=True
    )
    
    if exclude_user:
        users = users.exclude(id=exclude_user.id)
    
    return create_bulk_notifications(
        recipients=users,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url,
        action_label=action_label
    )


def notify_role(role, title, message, notification_type='info',
               action_url='', action_label='', exclude_user=None):
    """
    Send notification to all users with a specific role.
    """
    users = User.objects.filter(
        role=role,
        is_active=True,
        is_approved=True
    )
    
    if exclude_user:
        users = users.exclude(id=exclude_user.id)
    
    return create_bulk_notifications(
        recipients=users,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url,
        action_label=action_label
    )


def send_email_notification(notification):
    """
    Send email notification if user preferences allow it.
    """
    try:
        preferences = notification.recipient.notification_preferences
        
        # Check if email notifications are enabled
        if not preferences.should_send_notification(
            notification.notification_type, 
            'email'
        ):
            return False
        
        subject = f"[Office Management] {notification.title}"
        
        context = {
            'notification': notification,
            'user': notification.recipient,
            'action_url': notification.action_url,
        }
        
        html_message = render_to_string('emails/notification.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        notification.mark_as_sent()
        return True
        
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")
        return False


def cleanup_old_notifications(days=30):
    """
    Clean up old read notifications.
    """
    from django.utils import timezone
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=days)
    
    deleted_count = Notification.objects.filter(
        is_read=True,
        read_at__lt=cutoff_date
    ).delete()[0]
    
    return deleted_count


def get_notification_stats(user):
    """
    Get notification statistics for a user.
    """
    notifications = Notification.objects.filter(recipient=user)
    
    return {
        'total': notifications.count(),
        'unread': notifications.filter(is_read=False).count(),
        'by_type': {
            'info': notifications.filter(notification_type='info').count(),
            'success': notifications.filter(notification_type='success').count(),
            'warning': notifications.filter(notification_type='warning').count(),
            'error': notifications.filter(notification_type='error').count(),
            'task': notifications.filter(notification_type='task').count(),
            'attendance': notifications.filter(notification_type='attendance').count(),
            'salary': notifications.filter(notification_type='salary').count(),
            'learning': notifications.filter(notification_type='learning').count(),
            'system': notifications.filter(notification_type='system').count(),
        }
    }


# Predefined notification templates
NOTIFICATION_TEMPLATES = {
    'task_assigned': {
        'title': 'New Task Assigned',
        'message': 'You have been assigned a new task: {task_title}',
        'type': 'task',
        'action_label': 'View Task'
    },
    'task_completed': {
        'title': 'Task Completed',
        'message': 'Task "{task_title}" has been marked as completed',
        'type': 'success',
        'action_label': 'View Task'
    },
    'leave_approved': {
        'title': 'Leave Request Approved',
        'message': 'Your leave request from {start_date} to {end_date} has been approved',
        'type': 'success',
        'action_label': 'View Leave Requests'
    },
    'leave_rejected': {
        'title': 'Leave Request Rejected',
        'message': 'Your leave request from {start_date} to {end_date} has been rejected',
        'type': 'warning',
        'action_label': 'View Leave Requests'
    },
    'attendance_reminder': {
        'title': 'Attendance Reminder',
        'message': 'Don\'t forget to mark your attendance for today',
        'type': 'info',
        'action_label': 'Mark Attendance'
    },
    'salary_processed': {
        'title': 'Salary Processed',
        'message': 'Your salary for {month} {year} has been processed',
        'type': 'success',
        'action_label': 'View Payslip'
    },
    'course_enrolled': {
        'title': 'Course Enrollment Confirmed',
        'message': 'You have been successfully enrolled in "{course_title}"',
        'type': 'success',
        'action_label': 'View Course'
    },
    'training_session': {
        'title': 'Training Session Reminder',
        'message': 'You have a training session "{session_title}" scheduled for {datetime}',
        'type': 'info',
        'action_label': 'View Session'
    }
}


def create_templated_notification(recipient, template_key, context=None, **kwargs):
    """
    Create notification using predefined template.
    """
    if template_key not in NOTIFICATION_TEMPLATES:
        raise ValueError(f"Unknown notification template: {template_key}")
    
    template = NOTIFICATION_TEMPLATES[template_key]
    context = context or {}
    
    # Format message with context
    message = template['message'].format(**context)
    
    return create_notification(
        recipient=recipient,
        title=template['title'],
        message=message,
        notification_type=template['type'],
        action_label=template['action_label'],
        **kwargs
    )
