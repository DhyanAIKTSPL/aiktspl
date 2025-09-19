"""
Task management API views.
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.permissions import IsAdminUser, IsEmployeeOrAdmin
from .models import Project, Task, TaskComment
from .serializers import ProjectSerializer, TaskSerializer, TaskCommentSerializer


class ProjectListCreateView(generics.ListCreateAPIView):
    """List and create projects"""
    
    queryset = Project.objects.select_related('manager').prefetch_related('team_members')
    serializer_class = ProjectSerializer
    permission_classes = [IsEmployeeOrAdmin]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsEmployeeOrAdmin()]


class TaskListCreateView(generics.ListCreateAPIView):
    """List and create tasks"""
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Task.objects.select_related('assigned_to', 'assigned_by', 'project')
        return Task.objects.filter(assigned_to=self.request.user).select_related('assigned_by', 'project')
    
    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, delete task"""
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def complete_task(request, pk):
    """Mark task as completed"""
    
    try:
        task = Task.objects.get(pk=pk, assigned_to=request.user)
        completion_notes = request.data.get('completion_notes', '')
        task.mark_completed(completion_notes)
        
        return Response({
            'message': 'Task marked as completed',
            'task': TaskSerializer(task).data
        })
    
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


class TaskCommentListCreateView(generics.ListCreateAPIView):
    """List and create task comments"""
    
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return TaskComment.objects.filter(task_id=task_id).select_related('user')
    
    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        serializer.save(user=self.request.user, task_id=task_id)
