"""
Attendance tracking models for employee time management.
MongoDB-compatible using djongo.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime, time


class AttendanceRecord(models.Model):
    """
    Daily attendance records for employees.
    Tracks check-in, check-out, and work hours.
    MongoDB-compatible with djongo.
    """
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('work_from_home', 'Work From Home'),
    ]
    
    user_id = models.CharField(max_length=24, help_text="ObjectId reference to User")
    
    date = models.DateField(default=timezone.now)
    
    # Time tracking
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    
    # Status and hours
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    
    # Location tracking (optional)
    check_in_location = models.CharField(max_length=200, blank=True)
    check_out_location = models.CharField(max_length=200, blank=True)
    
    # Notes and approvals
    notes = models.TextField(blank=True)
    approved_by_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId of approving user")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        ordering = ['-date']
    
    def __str__(self):
        user = self.get_user()
        user_name = user.get_full_name() if user else "Unknown User"
        return f"{user_name} - {self.date} ({self.status})"
    
    def get_user(self):
        """Helper method to get the associated user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
    
    def get_approved_by(self):
        """Helper method to get the approving user"""
        if self.approved_by_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.approved_by_id)
            except User.DoesNotExist:
                return None
        return None
    
    def calculate_hours_worked(self):
        """Calculate hours worked based on check-in and check-out times"""
        if self.check_in_time and self.check_out_time:
            # Convert times to datetime for calculation
            check_in = datetime.combine(self.date, self.check_in_time)
            check_out = datetime.combine(self.date, self.check_out_time)
            
            # Handle overnight shifts
            if check_out < check_in:
                check_out = datetime.combine(self.date + timezone.timedelta(days=1), self.check_out_time)
            
            duration = check_out - check_in
            hours = duration.total_seconds() / 3600
            
            # Standard work day is 8 hours
            standard_hours = 8
            if hours > standard_hours:
                self.hours_worked = standard_hours
                self.overtime_hours = hours - standard_hours
            else:
                self.hours_worked = hours
                self.overtime_hours = 0
            
            self.save()
            return hours
        return 0


class LeaveRequest(models.Model):
    """
    Employee leave requests and approvals.
    MongoDB-compatible with djongo.
    """
    
    LEAVE_TYPES = [
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation'),
        ('personal', 'Personal Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('emergency', 'Emergency Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    user_id = models.CharField(max_length=24, help_text="ObjectId reference to User")
    
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Approval workflow
    approved_by_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId of approving user")
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Supporting documents
    supporting_document = models.FileField(upload_to='leave_documents/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'
        ordering = ['-created_at']
    
    def __str__(self):
        user = self.get_user()
        user_name = user.get_full_name() if user else "Unknown User"
        return f"{user_name} - {self.leave_type} ({self.start_date} to {self.end_date})"
    
    def get_user(self):
        """Helper method to get the associated user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
    
    def get_approved_by(self):
        """Helper method to get the approving user"""
        if self.approved_by_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.approved_by_id)
            except User.DoesNotExist:
                return None
        return None
    
    @property
    def duration_days(self):
        """Calculate leave duration in days"""
        return (self.end_date - self.start_date).days + 1
    
    def approve(self, approved_by_user):
        """Approve the leave request"""
        self.status = 'approved'
        self.approved_by_id = str(approved_by_user.id)
        self.approved_at = timezone.now()
        self.save()
    
    def reject(self, rejected_by_user, reason):
        """Reject the leave request"""
        self.status = 'rejected'
        self.approved_by_id = str(rejected_by_user.id)
        self.approved_at = timezone.now()
        self.rejection_reason = reason
        self.save()
