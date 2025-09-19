"""
Employee management models for organizational structure and departments.
MongoDB-compatible using djongo.
"""

from django.db import models
from django.conf import settings
from djongo import models as djongo_models


class Department(models.Model):
    """
    Department model for organizing employees.
    MongoDB-compatible with djongo.
    """
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    head_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId of department head")
    
    # Budget and operational details
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_head(self):
        """Helper method to get the department head"""
        if self.head_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.head_id)
            except User.DoesNotExist:
                return None
        return None
    
    @property
    def employee_count(self):
        """Get total number of employees in this department"""
        return EmployeeDetail.objects.filter(department_id=str(self.id)).count()


class Position(models.Model):
    """
    Job positions within the organization.
    MongoDB-compatible with djongo.
    """
    
    title = models.CharField(max_length=100)
    
    department_id = models.CharField(max_length=24, help_text="ObjectId reference to Department")
    description = models.TextField(blank=True)
    
    # Salary range
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Requirements
    required_skills = models.TextField(blank=True, help_text="Comma-separated list of required skills")
    experience_required = models.PositiveIntegerField(default=0, help_text="Years of experience required")
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'
        ordering = ['title']
    
    def __str__(self):
        department = self.get_department()
        dept_name = department.name if department else "Unknown Department"
        return f"{self.title} - {dept_name}"
    
    def get_department(self):
        """Helper method to get the associated department"""
        try:
            return Department.objects.get(id=self.department_id)
        except Department.DoesNotExist:
            return None


class EmployeeDetail(models.Model):
    """
    Extended employee information and work details.
    MongoDB-compatible with djongo.
    """
    
    user_id = models.CharField(max_length=24, unique=True, help_text="ObjectId reference to User")
    
    # Work assignment
    department_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to Department")
    position_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to Position")
    
    # Manager relationship
    manager_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to manager User")
    
    # Work schedule
    work_schedule = models.CharField(
        max_length=20,
        choices=[
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('contract', 'Contract'),
            ('intern', 'Intern'),
        ],
        default='full_time'
    )
    
    # Performance tracking
    performance_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Performance rating out of 5.00"
    )
    last_review_date = models.DateField(null=True, blank=True)
    next_review_date = models.DateField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Employee Detail'
        verbose_name_plural = 'Employee Details'
    
    def __str__(self):
        user = self.get_user()
        position = self.get_position()
        user_name = user.get_full_name() if user else "Unknown User"
        position_title = position.title if position else "No Position"
        return f"{user_name} - {position_title}"
    
    def get_user(self):
        """Helper method to get the associated user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
    
    def get_department(self):
        """Helper method to get the associated department"""
        if self.department_id:
            try:
                return Department.objects.get(id=self.department_id)
            except Department.DoesNotExist:
                return None
        return None
    
    def get_position(self):
        """Helper method to get the associated position"""
        if self.position_id:
            try:
                return Position.objects.get(id=self.position_id)
            except Position.DoesNotExist:
                return None
        return None
    
    def get_manager(self):
        """Helper method to get the manager"""
        if self.manager_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.manager_id)
            except User.DoesNotExist:
                return None
        return None
