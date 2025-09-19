"""
Notification system models for real-time updates.
MongoDB-compatible using djongo.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from djongo import models as djongo_models


class Notification(models.Model):
    """
    System notifications for users.
    MongoDB-compatible with djongo.
    """
    
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('task', 'Task Update'),
        ('attendance', 'Attendance'),
        ('salary', 'Salary'),
        ('learning', 'Learning'),
        ('system', 'System'),
    ]
    
    recipient_id = models.CharField(max_length=24, help_text="ObjectId reference to recipient User")
    
    # Notification content
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    
    # Metadata
    data = djongo_models.JSONField(default=dict, blank=True, help_text="Additional data for the notification")
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Actions
    action_url = models.URLField(blank=True, help_text="URL to navigate when notification is clicked")
    action_label = models.CharField(max_length=50, blank=True)
    
    # Delivery
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        recipient = self.get_recipient()
        recipient_name = recipient.get_full_name() if recipient else "Unknown User"
        return f"{self.title} - {recipient_name}"
    
    def get_recipient(self):
        """Helper method to get the recipient user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.recipient_id)
        except User.DoesNotExist:
            return None
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
    
    def mark_as_sent(self):
        """Mark notification as sent"""
        if not self.is_sent:
            self.is_sent = True
            self.sent_at = timezone.now()
            self.save()


class NotificationPreference(models.Model):
    """
    User preferences for notification delivery.
    MongoDB-compatible with djongo.
    """
    
    user_id = models.CharField(max_length=24, unique=True, help_text="ObjectId reference to User")
    
    # Email notifications
    email_enabled = models.BooleanField(default=True)
    email_task_updates = models.BooleanField(default=True)
    email_attendance_reminders = models.BooleanField(default=True)
    email_salary_updates = models.BooleanField(default=True)
    email_learning_updates = models.BooleanField(default=True)
    email_system_updates = models.BooleanField(default=True)
    
    # Push notifications (for future mobile app)
    push_enabled = models.BooleanField(default=True)
    push_task_updates = models.BooleanField(default=True)
    push_attendance_reminders = models.BooleanField(default=True)
    push_salary_updates = models.BooleanField(default=False)
    push_learning_updates = models.BooleanField(default=True)
    push_system_updates = models.BooleanField(default=True)
    
    # In-app notifications
    inapp_enabled = models.BooleanField(default=True)
    inapp_task_updates = models.BooleanField(default=True)
    inapp_attendance_reminders = models.BooleanField(default=True)
    inapp_salary_updates = models.BooleanField(default=True)
    inapp_learning_updates = models.BooleanField(default=True)
    inapp_system_updates = models.BooleanField(default=True)
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        user = self.get_user()
        user_name = user.get_full_name() if user else "Unknown User"
        return f"{user_name}'s Notification Preferences"
    
    def get_user(self):
        """Helper method to get the associated user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
    
    def should_send_notification(self, notification_type, delivery_method='inapp'):
        """Check if notification should be sent based on user preferences"""
        if delivery_method == 'email' and not self.email_enabled:
            return False
        elif delivery_method == 'push' and not self.push_enabled:
            return False
        elif delivery_method == 'inapp' and not self.inapp_enabled:
            return False
        
        # Check specific notification type preferences
        type_mapping = {
            'task': f'{delivery_method}_task_updates',
            'attendance': f'{delivery_method}_attendance_reminders',
            'salary': f'{delivery_method}_salary_updates',
            'learning': f'{delivery_method}_learning_updates',
            'system': f'{delivery_method}_system_updates',
        }
        
        if notification_type in type_mapping:
            return getattr(self, type_mapping[notification_type], True)
        
        return True


class SystemAnnouncement(models.Model):
    """
    System-wide announcements for all users.
    MongoDB-compatible with djongo.
    """
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Targeting
    target_roles = djongo_models.JSONField(
        default=list,
        blank=True,
        help_text="List of roles to target (empty = all users)"
    )
    target_departments = djongo_models.JSONField(
        default=list,
        blank=True,
        help_text="List of departments to target (empty = all departments)"
    )
    
    # Scheduling
    publish_at = models.DateTimeField(default=timezone.now)
    expire_at = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    
    # Creator
    created_by_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to creator User")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System Announcement'
        verbose_name_plural = 'System Announcements'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_created_by(self):
        """Helper method to get the creator user"""
        if self.created_by_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.created_by_id)
            except User.DoesNotExist:
                return None
        return None
    
    @property
    def is_expired(self):
        """Check if announcement has expired"""
        return self.expire_at and self.expire_at < timezone.now()
    
    def should_show_to_user(self, user):
        """Check if announcement should be shown to specific user"""
        if not self.is_active or not self.is_published or self.is_expired:
            return False
        
        # Check role targeting
        if self.target_roles and user.role not in self.target_roles:
            return False
        
        # Check department targeting
        if self.target_departments:
            try:
                from employees.models import EmployeeDetail
                employee_detail = EmployeeDetail.objects.get(user_id=str(user.id))
                user_dept = employee_detail.get_department()
                if user_dept and user_dept.name not in self.target_departments:
                    return False
            except EmployeeDetail.DoesNotExist:
                # If no employee detail, skip department check
                pass
        
        return True
