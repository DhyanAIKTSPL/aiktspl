"""
URL patterns for learning management APIs.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseListCreateView.as_view(), name='course_list'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('enrollments/', views.CourseEnrollmentListCreateView.as_view(), name='course_enrollments'),
    path('learning-paths/', views.LearningPathListView.as_view(), name='learning_paths'),
    path('training-sessions/', views.TrainingSessionListCreateView.as_view(), name='training_sessions'),
]
