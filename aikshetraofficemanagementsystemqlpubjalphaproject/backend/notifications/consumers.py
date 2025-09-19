"""
WebSocket consumers for real-time functionality.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications.
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group_name = f'user_{self.user_id}'
        
        # Verify user authentication
        user = await self.get_user(self.user_id)
        if not user:
            await self.close()
            return
        
        # Join user-specific group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial unread notification count
        unread_count = await self.get_unread_count(user)
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': unread_count
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle messages from WebSocket"""
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            if message_type == 'mark_read':
                notification_id = text_data_json.get('notification_id')
                await self.mark_notification_read(notification_id)
            
            elif message_type == 'get_notifications':
                notifications = await self.get_recent_notifications()
                await self.send(text_data=json.dumps({
                    'type': 'notifications_list',
                    'notifications': notifications
                }))
        
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))
    
    async def notification_message(self, event):
        """Send notification to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'notification': event['notification']
        }))
    
    async def unread_count_update(self, event):
        """Send updated unread count"""
        await self.send(text_data=json.dumps({
            'type': 'unread_count',
            'count': event['count']
        }))
    
    @database_sync_to_async
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_unread_count(self, user):
        """Get unread notification count"""
        return Notification.objects.filter(recipient=user, is_read=False).count()
    
    @database_sync_to_async
    def get_recent_notifications(self):
        """Get recent notifications for user"""
        user = User.objects.get(id=self.user_id)
        notifications = Notification.objects.filter(
            recipient=user
        ).order_by('-created_at')[:20]
        
        return [{
            'id': notif.id,
            'title': notif.title,
            'message': notif.message,
            'type': notif.notification_type,
            'is_read': notif.is_read,
            'created_at': notif.created_at.isoformat(),
            'action_url': notif.action_url,
            'action_label': notif.action_label,
        } for notif in notifications]
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark notification as read"""
        try:
            user = User.objects.get(id=self.user_id)
            notification = Notification.objects.get(
                id=notification_id,
                recipient=user
            )
            notification.mark_as_read()
            return True
        except (User.DoesNotExist, Notification.DoesNotExist):
            return False


class AttendanceConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time attendance updates.
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.attendance_group_name = f'attendance_{self.user_id}'
        
        # Verify user authentication
        user = await self.get_user(self.user_id)
        if not user:
            await self.close()
            return
        
        # Join attendance group
        await self.channel_layer.group_add(
            self.attendance_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.attendance_group_name,
            self.channel_name
        )
    
    async def attendance_update(self, event):
        """Send attendance update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'attendance_update',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class TaskConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time task updates.
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.task_group_name = f'tasks_{self.user_id}'
        
        # Verify user authentication
        user = await self.get_user(self.user_id)
        if not user:
            await self.close()
            return
        
        # Join task group
        await self.channel_layer.group_add(
            self.task_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.task_group_name,
            self.channel_name
        )
    
    async def task_update(self, event):
        """Send task update to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'task_update',
            'data': event['data']
        }))
    
    async def task_assigned(self, event):
        """Send task assignment notification"""
        await self.send(text_data=json.dumps({
            'type': 'task_assigned',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


class SystemConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for system-wide announcements.
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.system_group_name = 'system_announcements'
        
        # Join system announcements group
        await self.channel_layer.group_add(
            self.system_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.system_group_name,
            self.channel_name
        )
    
    async def system_announcement(self, event):
        """Send system announcement to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'system_announcement',
            'data': event['data']
        }))
