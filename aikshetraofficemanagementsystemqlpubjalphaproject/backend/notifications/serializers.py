"""
Serializers for notification management.
"""

from rest_framework import serializers
from .models import Notification, NotificationPreference, SystemAnnouncement


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications"""
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['recipient', 'is_sent', 'sent_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for notification preferences"""
    
    class Meta:
        model = NotificationPreference
        fields = '__all__'
        read_only_fields = ['user']


class SystemAnnouncementSerializer(serializers.ModelSerializer):
    """Serializer for system announcements"""
    
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = SystemAnnouncement
        fields = '__all__'
        read_only_fields = ['created_by']
