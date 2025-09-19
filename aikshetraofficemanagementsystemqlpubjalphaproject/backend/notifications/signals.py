"""
Django signals for real-time notifications.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from .models import Notification, SystemAnnouncement
from tasks.models import Task
from attendance.models import AttendanceRecord, LeaveRequest


channel_layer = get_channel_layer()


@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    """
    Send real-time notification when a new notification is created.
    """
    if created:
        # Send to user's notification group
        user_group_name = f'user_{instance.recipient.id}'
        
        notification_data = {
            'id': instance.id,
            'title': instance.title,
            'message': instance.message,
            'type': instance.notification_type,
            'is_read': instance.is_read,
            'created_at': instance.created_at.isoformat(),
            'action_url': instance.action_url,
            'action_label': instance.action_label,
        }
        
        async_to_sync(channel_layer.group_send)(
            user_group_name,
            {
                'type': 'notification_message',
                'notification': notification_data
            }
        )
        
        # Update unread count
        unread_count = Notification.objects.filter(
            recipient=instance.recipient,
            is_read=False
        ).count()
        
        async_to_sync(channel_layer.group_send)(
            user_group_name,
            {
                'type': 'unread_count_update',
                'count': unread_count
            }
        )


@receiver(post_save, sender=Task)
def task_updated(sender, instance, created, **kwargs):
    """
    Send real-time update when a task is created or updated.
    """
    task_group_name = f'tasks_{instance.assigned_to.id}'
    
    task_data = {
        'id': instance.id,
        'title': instance.title,
        'status': instance.status,
        'priority': instance.priority,
        'due_date': instance.due_date.isoformat(),
        'completion_percentage': instance.completion_percentage,
        'assigned_by': instance.assigned_by.get_full_name() if instance.assigned_by else None,
    }
    
    if created:
        # New task assigned
        async_to_sync(channel_layer.group_send)(
            task_group_name,
            {
                'type': 'task_assigned',
                'data': task_data
            }
        )
        
        # Create notification for task assignment
        Notification.objects.create(
            recipient=instance.assigned_to,
            title='New Task Assigned',
            message=f'You have been assigned a new task: {instance.title}',
            notification_type='task',
            action_url=f'/tasks/{instance.id}',
            action_label='View Task'
        )
    else:
        # Task updated
        async_to_sync(channel_layer.group_send)(
            task_group_name,
            {
                'type': 'task_update',
                'data': task_data
            }
        )


@receiver(post_save, sender=AttendanceRecord)
def attendance_updated(sender, instance, created, **kwargs):
    """
    Send real-time update when attendance is recorded.
    """
    attendance_group_name = f'attendance_{instance.user.id}'
    
    attendance_data = {
        'id': instance.id,
        'date': instance.date.isoformat(),
        'status': instance.status,
        'check_in_time': instance.check_in_time.strftime('%H:%M:%S') if instance.check_in_time else None,
        'check_out_time': instance.check_out_time.strftime('%H:%M:%S') if instance.check_out_time else None,
        'hours_worked': float(instance.hours_worked),
    }
    
    async_to_sync(channel_layer.group_send)(
        attendance_group_name,
        {
            'type': 'attendance_update',
            'data': attendance_data
        }
    )


@receiver(post_save, sender=LeaveRequest)
def leave_request_updated(sender, instance, created, **kwargs):
    """
    Send notification when leave request status changes.
    """
    if not created and instance.status in ['approved', 'rejected']:
        # Notify employee about leave request decision
        status_text = 'approved' if instance.status == 'approved' else 'rejected'
        
        Notification.objects.create(
            recipient=instance.user,
            title=f'Leave Request {status_text.title()}',
            message=f'Your leave request from {instance.start_date} to {instance.end_date} has been {status_text}.',
            notification_type='info',
            action_url='/employee/leave-requests',
            action_label='View Leave Requests'
        )


@receiver(post_save, sender=SystemAnnouncement)
def system_announcement_created(sender, instance, created, **kwargs):
    """
    Broadcast system announcement to all connected users.
    """
    if created and instance.is_published:
        announcement_data = {
            'id': instance.id,
            'title': instance.title,
            'content': instance.content,
            'priority': instance.priority,
            'created_at': instance.created_at.isoformat(),
        }
        
        async_to_sync(channel_layer.group_send)(
            'system_announcements',
            {
                'type': 'system_announcement',
                'data': announcement_data
            }
        )
