"""
Serializers for task management.
"""

from rest_framework import serializers
from .models import Project, Task, TaskComment


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project management"""
    
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    team_member_names = serializers.SerializerMethodField()
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def get_team_member_names(self, obj):
        return [member.get_full_name() for member in obj.team_members.all()]


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for task management"""
    
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.get_full_name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['completed_at']


class TaskCommentSerializer(serializers.ModelSerializer):
    """Serializer for task comments"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = TaskComment
        fields = '__all__'
        read_only_fields = ['user']
