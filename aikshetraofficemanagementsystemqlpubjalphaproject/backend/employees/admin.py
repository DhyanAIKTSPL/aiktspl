"""
Django admin for employee management.
"""

from django.contrib import admin
from .models import Department, Position, EmployeeDetail


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head', 'employee_count', 'budget', 'location', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['name', 'description']
    
    def employee_count(self, obj):
        return obj.employee_count
    employee_count.short_description = 'Employees'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'min_salary', 'max_salary', 'experience_required', 'is_active']
    list_filter = ['department', 'is_active', 'experience_required']
    search_fields = ['title', 'description', 'required_skills']


@admin.register(EmployeeDetail)
class EmployeeDetailAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'position', 'manager', 'work_schedule', 'performance_rating', 'is_active']
    list_filter = ['department', 'position', 'work_schedule', 'is_active']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'department', 'position', 'manager')
