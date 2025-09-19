"""
Attendance management API views.
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from accounts.permissions import IsAdminUser, IsOwnerOrAdmin
from .models import AttendanceRecord, LeaveRequest
from .serializers import AttendanceRecordSerializer, LeaveRequestSerializer


class AttendanceRecordListCreateView(generics.ListCreateAPIView):
    """List and create attendance records"""
    
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return AttendanceRecord.objects.select_related('user', 'approved_by')
        return AttendanceRecord.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_in(request):
    """Check-in endpoint"""
    
    today = timezone.now().date()
    user = request.user
    
    # Check if already checked in today
    existing_record = AttendanceRecord.objects.filter(user=user, date=today).first()
    if existing_record and existing_record.check_in_time:
        return Response({
            'error': 'Already checked in today'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create or update attendance record
    if existing_record:
        existing_record.check_in_time = timezone.now().time()
        existing_record.status = 'present'
        existing_record.save()
        record = existing_record
    else:
        record = AttendanceRecord.objects.create(
            user=user,
            date=today,
            check_in_time=timezone.now().time(),
            status='present'
        )
    
    return Response({
        'message': 'Checked in successfully',
        'check_in_time': record.check_in_time.strftime('%H:%M:%S')
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_out(request):
    """Check-out endpoint"""
    
    today = timezone.now().date()
    user = request.user
    
    record = AttendanceRecord.objects.filter(user=user, date=today).first()
    if not record or not record.check_in_time:
        return Response({
            'error': 'No check-in record found for today'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if record.check_out_time:
        return Response({
            'error': 'Already checked out today'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    record.check_out_time = timezone.now().time()
    record.calculate_hours_worked()
    
    return Response({
        'message': 'Checked out successfully',
        'check_out_time': record.check_out_time.strftime('%H:%M:%S'),
        'hours_worked': float(record.hours_worked)
    })


class LeaveRequestListCreateView(generics.ListCreateAPIView):
    """List and create leave requests"""
    
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return LeaveRequest.objects.select_related('user', 'approved_by')
        return LeaveRequest.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_leave(request, pk):
    """Approve leave request"""
    
    try:
        leave_request = LeaveRequest.objects.get(pk=pk)
        action = request.data.get('action')
        
        if action == 'approve':
            leave_request.approve(request.user)
            message = 'Leave request approved'
        elif action == 'reject':
            reason = request.data.get('reason', '')
            leave_request.reject(request.user, reason)
            message = 'Leave request rejected'
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': message,
            'leave_request': LeaveRequestSerializer(leave_request).data
        })
    
    except LeaveRequest.DoesNotExist:
        return Response({'error': 'Leave request not found'}, status=status.HTTP_404_NOT_FOUND)
