"""
Notification management API views.
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.permissions import IsAdminUser
from .models import Notification, NotificationPreference, SystemAnnouncement
from .serializers import NotificationSerializer, NotificationPreferenceSerializer, SystemAnnouncementSerializer


class NotificationListView(generics.ListAPIView):
    """List user notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    """Mark notification as read"""
    
    try:
        notification = Notification.objects.get(pk=pk, recipient=request.user)
        notification.mark_as_read()
        
        return Response({
            'message': 'Notification marked as read'
        })
    
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)


class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    """Get and update notification preferences"""
    
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preference, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preference


class SystemAnnouncementListCreateView(generics.ListCreateAPIView):
    """List and create system announcements"""
    
    serializer_class = SystemAnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return SystemAnnouncement.objects.all()
        
        # Return announcements visible to current user
        announcements = SystemAnnouncement.objects.filter(
            is_active=True,
            is_published=True
        )
        
        visible_announcements = []
        for announcement in announcements:
            if announcement.should_show_to_user(self.request.user):
                visible_announcements.append(announcement.id)
        
        return SystemAnnouncement.objects.filter(id__in=visible_announcements)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
