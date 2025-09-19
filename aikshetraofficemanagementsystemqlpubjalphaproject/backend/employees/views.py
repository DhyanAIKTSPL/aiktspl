"""
Employee management API views.
"""

from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.permissions import IsAdminUser, IsEmployeeOrAdmin
from .models import Department, Position, EmployeeDetail
from .serializers import DepartmentSerializer, PositionSerializer, EmployeeDetailSerializer


class DepartmentListCreateView(generics.ListCreateAPIView):
    """List and create departments"""
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsEmployeeOrAdmin]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsEmployeeOrAdmin()]


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, delete department"""
    
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]


class PositionListCreateView(generics.ListCreateAPIView):
    """List and create positions"""
    
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsEmployeeOrAdmin]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsEmployeeOrAdmin()]


class EmployeeDetailListView(generics.ListAPIView):
    """List employee details"""
    
    queryset = EmployeeDetail.objects.select_related('user', 'department', 'position', 'manager')
    serializer_class = EmployeeDetailSerializer
    permission_classes = [IsEmployeeOrAdmin]
