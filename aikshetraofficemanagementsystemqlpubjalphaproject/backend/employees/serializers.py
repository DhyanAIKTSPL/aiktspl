"""
Serializers for employee management.
"""

from rest_framework import serializers
from .models import Department, Position, EmployeeDetail
from accounts.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for department management"""
    
    employee_count = serializers.ReadOnlyField()
    head_name = serializers.CharField(source='head.get_full_name', read_only=True)
    
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    """Serializer for position management"""
    
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Position
        fields = '__all__'


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Serializer for employee details"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta:
        model = EmployeeDetail
        fields = '__all__'
