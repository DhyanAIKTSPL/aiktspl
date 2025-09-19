"""
URL patterns for notification management APIs.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification_list'),
    path('<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('preferences/', views.NotificationPreferenceView.as_view(), name='notification_preferences'),
    path('announcements/', views.SystemAnnouncementListCreateView.as_view(), name='system_announcements'),
]
