"""
Serializers for attendance management.
"""

from rest_framework import serializers
from .models import AttendanceRecord, LeaveRequest


class AttendanceRecordSerializer(serializers.ModelSerializer):
    """Serializer for attendance records"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = AttendanceRecord
        fields = '__all__'
        read_only_fields = ['hours_worked', 'overtime_hours']
    
    def create(self, validated_data):
        """Create attendance record and calculate hours"""
        record = super().create(validated_data)
        record.calculate_hours_worked()
        return record


class LeaveRequestSerializer(serializers.ModelSerializer):
    """Serializer for leave requests"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    duration_days = serializers.ReadOnlyField()
    
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ['approved_by', 'approved_at']
