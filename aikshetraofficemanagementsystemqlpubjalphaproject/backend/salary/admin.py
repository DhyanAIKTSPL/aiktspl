"""
Django admin for salary management.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import SalaryStructure, EmployeeSalary, Payroll


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'base_salary', 'gross_salary', 'total_deductions', 
        'net_salary', 'is_active'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Salary Components', {
            'fields': ('base_salary', 'house_rent_allowance', 'transport_allowance', 'medical_allowance', 'other_allowances')
        }),
        ('Deductions', {
            'fields': ('provident_fund_percentage', 'tax_percentage', 'insurance_deduction', 'other_deductions')
        }),
    )


@admin.register(EmployeeSalary)
class EmployeeSalaryAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'salary_structure', 'current_base_salary', 
        'monthly_gross_salary', 'effective_from', 'is_active'
    ]
    list_filter = ['salary_structure', 'is_active', 'effective_from']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'salary_structure')


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'month', 'year', 'gross_salary', 'total_deductions', 
        'net_salary', 'status', 'payment_date'
    ]
    list_filter = ['status', 'year', 'month', 'payment_date']
    search_fields = ['user__first_name', 'user__last_name', 'transaction_reference']
    
    fieldsets = (
        ('Employee & Period', {
            'fields': ('user', 'month', 'year')
        }),
        ('Salary Components', {
            'fields': ('base_salary', 'allowances', 'overtime_amount', 'bonus')
        }),
        ('Deductions', {
            'fields': ('provident_fund', 'tax_deduction', 'insurance', 'other_deductions')
        }),
        ('Attendance', {
            'fields': ('days_worked', 'total_working_days', 'overtime_hours')
        }),
        ('Calculated Amounts', {
            'fields': ('gross_salary', 'total_deductions', 'net_salary'),
            'classes': ('collapse',)
        }),
        ('Processing', {
            'fields': ('status', 'processed_by', 'processed_at', 'notes')
        }),
        ('Payment', {
            'fields': ('payment_date', 'payment_method', 'transaction_reference'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['processed_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'processed_by')
