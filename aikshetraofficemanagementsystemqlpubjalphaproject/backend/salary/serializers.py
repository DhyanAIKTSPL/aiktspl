"""
Serializers for salary management.
"""

from rest_framework import serializers
from .models import SalaryStructure, EmployeeSalary, Payroll


class SalaryStructureSerializer(serializers.ModelSerializer):
    """Serializer for salary structures"""
    
    gross_salary = serializers.ReadOnlyField()
    total_deductions = serializers.ReadOnlyField()
    net_salary = serializers.ReadOnlyField()
    
    class Meta:
        model = SalaryStructure
        fields = '__all__'


class EmployeeSalarySerializer(serializers.ModelSerializer):
    """Serializer for employee salary assignments"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    structure_name = serializers.CharField(source='salary_structure.name', read_only=True)
    monthly_gross_salary = serializers.ReadOnlyField()
    
    class Meta:
        model = EmployeeSalary
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    """Serializer for payroll records"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    processed_by_name = serializers.CharField(source='processed_by.get_full_name', read_only=True)
    
    class Meta:
        model = Payroll
        fields = '__all__'
        read_only_fields = ['processed_by', 'processed_at']
