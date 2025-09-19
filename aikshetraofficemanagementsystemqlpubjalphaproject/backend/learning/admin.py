"""
Django admin for learning management.
"""

from django.contrib import admin
from .models import Course, CourseEnrollment, LearningPath, LearningPathCourse, TrainingSession, SessionAttendance


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'instructor', 'category', 'difficulty_level', 
        'duration_hours', 'enrollment_count', 'status', 'is_mandatory'
    ]
    list_filter = ['status', 'difficulty_level', 'category', 'is_mandatory']
    search_fields = ['title', 'description', 'category']
    
    def enrollment_count(self, obj):
        return obj.enrollment_count
    enrollment_count.short_description = 'Enrollments'


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'course', 'status', 'progress_percentage', 
        'enrolled_at', 'completed_at', 'final_score'
    ]
    list_filter = ['status', 'enrolled_at', 'completed_at']
    search_fields = ['user__first_name', 'user__last_name', 'course__title']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'course')


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['name', 'estimated_duration_weeks', 'is_mandatory', 'is_active']
    list_filter = ['is_mandatory', 'is_active']
    search_fields = ['name', 'description']
    filter_horizontal = ['courses']


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'instructor', 'start_datetime', 'end_datetime', 
        'participant_count', 'max_participants', 'status'
    ]
    list_filter = ['status', 'start_datetime']
    search_fields = ['title', 'description', 'instructor__first_name', 'instructor__last_name']
    
    def participant_count(self, obj):
        return obj.participant_count
    participant_count.short_description = 'Participants'


@admin.register(SessionAttendance)
class SessionAttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', 'status', 'registered_at', 'rating']
    list_filter = ['status', 'registered_at', 'rating']
    search_fields = ['user__first_name', 'user__last_name', 'session__title']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'session')
