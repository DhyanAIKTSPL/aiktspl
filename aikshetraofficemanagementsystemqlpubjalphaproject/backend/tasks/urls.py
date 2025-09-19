"""
URL patterns for task management APIs.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.ProjectListCreateView.as_view(), name='project_list'),
    path('', views.TaskListCreateView.as_view(), name='task_list'),
    path('<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:pk>/complete/', views.complete_task, name='complete_task'),
    path('<int:task_id>/comments/', views.TaskCommentListCreateView.as_view(), name='task_comments'),
]
