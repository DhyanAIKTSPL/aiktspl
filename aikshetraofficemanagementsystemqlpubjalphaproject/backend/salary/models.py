"""
Salary and payroll management models.
MongoDB-compatible using djongo.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


class SalaryStructure(models.Model):
    """
    Salary structure template for different positions and levels.
    MongoDB-compatible with djongo.
    """
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Base salary components
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    house_rent_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medical_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Deductions
    provident_fund_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    insurance_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Salary Structure'
        verbose_name_plural = 'Salary Structures'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def gross_salary(self):
        """Calculate gross salary"""
        return (
            self.base_salary + 
            self.house_rent_allowance + 
            self.transport_allowance + 
            self.medical_allowance + 
            self.other_allowances
        )
    
    @property
    def total_deductions(self):
        """Calculate total deductions"""
        pf_amount = (self.gross_salary * self.provident_fund_percentage) / 100
        tax_amount = (self.gross_salary * self.tax_percentage) / 100
        return pf_amount + tax_amount + self.insurance_deduction + self.other_deductions
    
    @property
    def net_salary(self):
        """Calculate net salary"""
        return self.gross_salary - self.total_deductions


class EmployeeSalary(models.Model):
    """
    Individual employee salary assignments.
    MongoDB-compatible with djongo.
    """
    
    user_id = models.CharField(max_length=24, unique=True, help_text="ObjectId reference to User")
    salary_structure_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to SalaryStructure")
    
    # Custom salary overrides
    custom_base_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    custom_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custom_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Effective dates
    effective_from = models.DateField(default=timezone.now)
    effective_to = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Employee Salary'
        verbose_name_plural = 'Employee Salaries'
    
    def __str__(self):
        user = self.get_user()
        user_name = user.get_full_name() if user else "Unknown User"
        return f"{user_name} - Salary"
    
    def get_user(self):
        """Helper method to get the associated user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
    
    def get_salary_structure(self):
        """Helper method to get the salary structure"""
        if self.salary_structure_id:
            try:
                return SalaryStructure.objects.get(id=self.salary_structure_id)
            except SalaryStructure.DoesNotExist:
                return None
        return None
    
    @property
    def current_base_salary(self):
        """Get current base salary (custom or from structure)"""
        if self.custom_base_salary:
            return self.custom_base_salary
        salary_structure = self.get_salary_structure()
        return salary_structure.base_salary if salary_structure else 0
    
    @property
    def monthly_gross_salary(self):
        """Calculate monthly gross salary"""
        salary_structure = self.get_salary_structure()
        if salary_structure:
            base = self.current_base_salary
            allowances = (
                salary_structure.house_rent_allowance +
                salary_structure.transport_allowance +
                salary_structure.medical_allowance +
                salary_structure.other_allowances +
                self.custom_allowances
            )
            return base + allowances
        return self.custom_base_salary or 0


class Payroll(models.Model):
    """
    Monthly payroll records for employees.
    MongoDB-compatible with djongo.
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('processed', 'Processed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    user_id = models.CharField(max_length=24, help_text="ObjectId reference to User")
    
    # Payroll period
    month = models.PositiveIntegerField()  # 1-12
    year = models.PositiveIntegerField()
    
    # Salary components
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Deductions
    provident_fund = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    insurance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Attendance impact
    days_worked = models.PositiveIntegerField(default=0)
    total_working_days = models.PositiveIntegerField(default=22)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Final amounts
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status and processing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    processed_by_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId of processing user")
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Payment details
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Payroll Record'
        verbose_name_plural = 'Payroll Records'
        ordering = ['-year', '-month']
    
    def __str__(self):
        user = self.get_user()
        user_name = user.get_full_name() if user else "Unknown User"
        return f"{user_name} - {self.month}/{self.year}"
    
    def get_user(self):
        """Helper method to get the associated user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
    
    def get_processed_by(self):
        """Helper method to get the processing user"""
        if self.processed_by_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.processed_by_id)
            except User.DoesNotExist:
                return None
        return None
    
    def calculate_amounts(self):
        """Calculate gross, deductions, and net salary"""
        self.gross_salary = self.base_salary + self.allowances + self.overtime_amount + self.bonus
        self.total_deductions = self.provident_fund + self.tax_deduction + self.insurance + self.other_deductions
        self.net_salary = self.gross_salary - self.total_deductions
        self.save()
