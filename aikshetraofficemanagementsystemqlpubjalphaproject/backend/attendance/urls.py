"""
URL patterns for attendance management APIs.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('records/', views.AttendanceRecordListCreateView.as_view(), name='attendance_records'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
    path('leave-requests/', views.LeaveRequestListCreateView.as_view(), name='leave_requests'),
    path('leave-requests/<int:pk>/approve/', views.approve_leave, name='approve_leave'),
]
