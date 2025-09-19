"""
Serializers for learning management.
"""

from rest_framework import serializers
from .models import Course, CourseEnrollment, LearningPath, TrainingSession, SessionAttendance


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for courses"""
    
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    enrollment_count = serializers.ReadOnlyField()
    is_enrollment_open = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = '__all__'


class CourseEnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for course enrollments"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = CourseEnrollment
        fields = '__all__'
        read_only_fields = ['user', 'completed_at']


class LearningPathSerializer(serializers.ModelSerializer):
    """Serializer for learning paths"""
    
    course_count = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningPath
        fields = '__all__'
    
    def get_course_count(self, obj):
        return obj.courses.count()


class TrainingSessionSerializer(serializers.ModelSerializer):
    """Serializer for training sessions"""
    
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    participant_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = TrainingSession
        fields = '__all__'


class SessionAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for session attendance"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    session_title = serializers.CharField(source='session.title', read_only=True)
    
    class Meta:
        model = SessionAttendance
        fields = '__all__'
        read_only_fields = ['user']
