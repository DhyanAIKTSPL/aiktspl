"""
User and authentication models for the office management system.
Supports admin, employee, and trainee roles with approval workflow.
MongoDB-compatible using djongo.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from djongo import models as djongo_models


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Supports role-based access control and approval workflow.
    MongoDB-compatible with djongo.
    """
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('trainee', 'Trainee'),
    ]
    
    # Basic user information
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, blank=True)
    
    # Role and approval system
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    is_approved = models.BooleanField(default=False, help_text="Admin approval required for login")
    
    approved_by_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId of admin who approved this user")
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Profile information
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    
    # Employment details
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True)
    position = models.CharField(max_length=50, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def approve_user(self, approved_by_user):
        """Approve user for system access"""
        self.is_approved = True
        self.approved_by_id = str(approved_by_user.id)
        self.approved_at = timezone.now()
        self.save()
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_employee(self):
        return self.role == 'employee'
    
    @property
    def is_trainee(self):
        return self.role == 'trainee'


class UserProfile(models.Model):
    """
    Extended profile information for users.
    Stores additional details not in the main User model.
    MongoDB-compatible with djongo.
    """
    
    user_id = models.CharField(max_length=24, unique=True, help_text="ObjectId reference to User")
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    # Skills and certifications
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    certifications = models.TextField(blank=True)
    
    # Social links
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Preferences
    notification_preferences = djongo_models.JSONField(default=dict, blank=True)
    theme_preference = models.CharField(
        max_length=10, 
        choices=[('light', 'Light'), ('dark', 'Dark')], 
        default='light'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile for user {self.user_id}"
    
    def get_user(self):
        """Helper method to get the associated user"""
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
