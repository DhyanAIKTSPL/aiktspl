"""
Task management models for project and work assignment tracking.
MongoDB-compatible using djongo.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from djongo import models as djongo_models


class Project(models.Model):
    """
    Project model for organizing tasks and work assignments.
    MongoDB-compatible with djongo.
    """
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    manager_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to manager User")
    team_member_ids = djongo_models.JSONField(default=list, blank=True, help_text="List of ObjectIds for team members")
    
    # Timeline and status
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Budget and progress
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    progress_percentage = models.PositiveIntegerField(default=0, help_text="Progress from 0 to 100")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_manager(self):
        """Helper method to get the project manager"""
        if self.manager_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.manager_id)
            except User.DoesNotExist:
                return None
        return None
    
    def get_team_members(self):
        """Helper method to get team members"""
        if self.team_member_ids:
            try:
                from accounts.models import User
                return User.objects.filter(id__in=self.team_member_ids)
            except:
                return []
        return []
    
    @property
    def is_overdue(self):
        """Check if project is overdue"""
        return self.end_date < timezone.now().date() and self.status not in ['completed', 'cancelled']
    
    @property
    def days_remaining(self):
        """Calculate days remaining for project completion"""
        if self.status in ['completed', 'cancelled']:
            return 0
        return (self.end_date - timezone.now().date()).days


class Task(models.Model):
    """
    Individual task model for work assignments.
    MongoDB-compatible with djongo.
    """
    
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    project_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to Project")
    assigned_to_id = models.CharField(max_length=24, help_text="ObjectId reference to assigned User")
    assigned_by_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to assigning User")
    
    # Timeline and status
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Progress tracking
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completion_percentage = models.PositiveIntegerField(default=0)
    
    # File attachments
    attachments = models.FileField(upload_to='task_attachments/', blank=True, null=True)
    
    # Completion details
    completed_at = models.DateTimeField(null=True, blank=True)
    completion_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']
    
    def __str__(self):
        assigned_user = self.get_assigned_to()
        user_name = assigned_user.get_full_name() if assigned_user else "Unknown User"
        return f"{self.title} - {user_name}"
    
    def get_project(self):
        """Helper method to get the associated project"""
        if self.project_id:
            try:
                return Project.objects.get(id=self.project_id)
            except Project.DoesNotExist:
                return None
        return None
    
    def get_assigned_to(self):
        """Helper method to get the assigned user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.assigned_to_id)
        except User.DoesNotExist:
            return None
    
    def get_assigned_by(self):
        """Helper method to get the assigning user"""
        if self.assigned_by_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.assigned_by_id)
            except User.DoesNotExist:
                return None
        return None
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        return self.due_date < timezone.now() and self.status not in ['completed', 'cancelled']
    
    def mark_completed(self, completion_notes=''):
        """Mark task as completed"""
        self.status = 'completed'
        self.completion_percentage = 100
        self.completed_at = timezone.now()
        self.completion_notes = completion_notes
        self.save()


class TaskComment(models.Model):
    """
    Comments and updates on tasks for collaboration.
    MongoDB-compatible with djongo.
    """
    
    task_id = models.CharField(max_length=24, help_text="ObjectId reference to Task")
    user_id = models.CharField(max_length=24, help_text="ObjectId reference to User")
    
    comment = models.TextField()
    attachment = models.FileField(upload_to='task_comments/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Task Comment'
        verbose_name_plural = 'Task Comments'
        ordering = ['-created_at']
    
    def __str__(self):
        task = self.get_task()
        user = self.get_user()
        task_title = task.title if task else "Unknown Task"
        user_name = user.get_full_name() if user else "Unknown User"
        return f"Comment on {task_title} by {user_name}"
    
    def get_task(self):
        """Helper method to get the associated task"""
        try:
            return Task.objects.get(id=self.task_id)
        except Task.DoesNotExist:
            return None
    
    def get_user(self):
        """Helper method to get the commenting user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
