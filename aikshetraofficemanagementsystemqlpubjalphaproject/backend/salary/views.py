"""
Salary management API views.
"""

from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.permissions import IsAdminUser
from .models import SalaryStructure, EmployeeSalary, Payroll
from .serializers import SalaryStructureSerializer, EmployeeSalarySerializer, PayrollSerializer


class SalaryStructureListCreateView(generics.ListCreateAPIView):
    """List and create salary structures"""
    
    queryset = SalaryStructure.objects.all()
    serializer_class = SalaryStructureSerializer
    permission_classes = [IsAdminUser]


class EmployeeSalaryListView(generics.ListAPIView):
    """List employee salaries"""
    
    serializer_class = EmployeeSalarySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return EmployeeSalary.objects.select_related('user', 'salary_structure')
        return EmployeeSalary.objects.filter(user=self.request.user)


class PayrollListCreateView(generics.ListCreateAPIView):
    """List and create payroll records"""
    
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Payroll.objects.select_related('user', 'processed_by')
        return Payroll.objects.filter(user=self.request.user)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        payroll = serializer.save(processed_by=self.request.user)
        payroll.calculate_amounts()
