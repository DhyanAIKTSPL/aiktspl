"""
Django admin for task management.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Task, TaskComment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'manager', 'status', 'priority', 'start_date', 
        'end_date', 'progress_percentage', 'is_overdue'
    ]
    list_filter = ['status', 'priority', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    filter_horizontal = ['team_members']
    date_hierarchy = 'start_date'
    
    def is_overdue(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red;">Yes</span>')
        return 'No'
    is_overdue.short_description = 'Overdue'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'assigned_to', 'project', 'status', 'priority', 
        'due_date', 'completion_percentage', 'is_overdue'
    ]
    list_filter = ['status', 'priority', 'project', 'due_date']
    search_fields = ['title', 'description', 'assigned_to__first_name', 'assigned_to__last_name']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Task Details', {
            'fields': ('title', 'description', 'project')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'assigned_by')
        }),
        ('Timeline & Priority', {
            'fields': ('due_date', 'status', 'priority')
        }),
        ('Progress Tracking', {
            'fields': ('estimated_hours', 'actual_hours', 'completion_percentage')
        }),
        ('Completion', {
            'fields': ('completed_at', 'completion_notes', 'attachments'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['completed_at']
    
    def is_overdue(self, obj):
        if obj.is_overdue:
            return format_html('<span style="color: red;">Yes</span>')
        return 'No'
    is_overdue.short_description = 'Overdue'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('assigned_to', 'assigned_by', 'project')


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'created_at']
    list_filter = ['created_at', 'task__project']
    search_fields = ['task__title', 'user__first_name', 'user__last_name', 'comment']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('task', 'user')
