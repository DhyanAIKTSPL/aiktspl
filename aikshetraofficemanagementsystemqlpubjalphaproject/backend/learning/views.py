"""
Learning management API views.
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.permissions import IsAdminUser, IsTraineeOrAbove
from .models import Course, CourseEnrollment, LearningPath, TrainingSession, SessionAttendance
from .serializers import (
    CourseSerializer, CourseEnrollmentSerializer, LearningPathSerializer,
    TrainingSessionSerializer, SessionAttendanceSerializer
)


class CourseListCreateView(generics.ListCreateAPIView):
    """List and create courses"""
    
    queryset = Course.objects.select_related('instructor')
    serializer_class = CourseSerializer
    permission_classes = [IsTraineeOrAbove]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsTraineeOrAbove()]


class CourseEnrollmentListCreateView(generics.ListCreateAPIView):
    """List and create course enrollments"""
    
    serializer_class = CourseEnrollmentSerializer
    permission_classes = [IsTraineeOrAbove]
    
    def get_queryset(self):
        if self.request.user.is_admin:
            return CourseEnrollment.objects.select_related('user', 'course')
        return CourseEnrollment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsTraineeOrAbove])
def enroll_course(request, course_id):
    """Enroll in a course"""
    
    try:
        course = Course.objects.get(pk=course_id)
        
        if not course.is_enrollment_open:
            return Response({
                'error': 'Enrollment is not open for this course'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        enrollment, created = CourseEnrollment.objects.get_or_create(
            user=request.user,
            course=course
        )
        
        if not created:
            return Response({
                'error': 'Already enrolled in this course'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': 'Successfully enrolled in course',
            'enrollment': CourseEnrollmentSerializer(enrollment).data
        })
    
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


class LearningPathListView(generics.ListAPIView):
    """List learning paths"""
    
    queryset = LearningPath.objects.filter(is_active=True)
    serializer_class = LearningPathSerializer
    permission_classes = [IsTraineeOrAbove]


class TrainingSessionListCreateView(generics.ListCreateAPIView):
    """List and create training sessions"""
    
    queryset = TrainingSession.objects.select_related('instructor', 'course')
    serializer_class = TrainingSessionSerializer
    permission_classes = [IsTraineeOrAbove]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsTraineeOrAbove()]
