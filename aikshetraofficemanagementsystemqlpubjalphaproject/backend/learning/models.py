"""
Learning and training management models.
MongoDB-compatible using djongo.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone
from djongo import models as djongo_models


class Course(models.Model):
    """
    Training courses and learning materials.
    MongoDB-compatible with djongo.
    """
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    instructor_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to instructor User")
    category = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    
    # Content and duration
    duration_hours = models.PositiveIntegerField(help_text="Course duration in hours")
    prerequisites = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    
    # Media and resources
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    course_materials = models.FileField(upload_to='course_materials/', blank=True, null=True)
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_mandatory = models.BooleanField(default=False)
    
    # Enrollment
    max_enrollments = models.PositiveIntegerField(null=True, blank=True)
    enrollment_deadline = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_instructor(self):
        """Helper method to get the instructor"""
        if self.instructor_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.instructor_id)
            except User.DoesNotExist:
                return None
        return None
    
    @property
    def enrollment_count(self):
        """Get current enrollment count"""
        return CourseEnrollment.objects.filter(course_id=str(self.id), status='enrolled').count()
    
    @property
    def is_enrollment_open(self):
        """Check if enrollment is still open"""
        if self.enrollment_deadline and self.enrollment_deadline < timezone.now():
            return False
        if self.max_enrollments and self.enrollment_count >= self.max_enrollments:
            return False
        return self.status == 'published'


class CourseEnrollment(models.Model):
    """
    Student enrollment in courses.
    MongoDB-compatible with djongo.
    """
    
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('failed', 'Failed'),
    ]
    
    user_id = models.CharField(max_length=24, help_text="ObjectId reference to User")
    course_id = models.CharField(max_length=24, help_text="ObjectId reference to Course")
    
    # Enrollment details
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    
    # Progress tracking
    progress_percentage = models.PositiveIntegerField(default=0)
    hours_completed = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # Completion details
    completed_at = models.DateTimeField(null=True, blank=True)
    final_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    certificate_issued = models.BooleanField(default=False)
    
    # Feedback
    rating = models.PositiveIntegerField(null=True, blank=True, help_text="Rating out of 5")
    feedback = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Course Enrollment'
        verbose_name_plural = 'Course Enrollments'
        ordering = ['-enrolled_at']
    
    def __str__(self):
        user = self.get_user()
        course = self.get_course()
        user_name = user.get_full_name() if user else "Unknown User"
        course_title = course.title if course else "Unknown Course"
        return f"{user_name} - {course_title}"
    
    def get_user(self):
        """Helper method to get the enrolled user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
    
    def get_course(self):
        """Helper method to get the course"""
        try:
            return Course.objects.get(id=self.course_id)
        except Course.DoesNotExist:
            return None
    
    def mark_completed(self, final_score=None):
        """Mark enrollment as completed"""
        self.status = 'completed'
        self.progress_percentage = 100
        self.completed_at = timezone.now()
        if final_score:
            self.final_score = final_score
        self.save()


class LearningPath(models.Model):
    """
    Structured learning paths with multiple courses.
    MongoDB-compatible with djongo.
    """
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    course_ids = djongo_models.JSONField(default=list, blank=True, help_text="List of ObjectIds for courses in order")
    target_audience = models.CharField(max_length=100, blank=True)
    estimated_duration_weeks = models.PositiveIntegerField()
    
    # Requirements
    prerequisites = models.TextField(blank=True)
    is_mandatory = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Learning Path'
        verbose_name_plural = 'Learning Paths'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_courses(self):
        """Helper method to get courses in the learning path"""
        if self.course_ids:
            try:
                return Course.objects.filter(id__in=self.course_ids)
            except:
                return []
        return []


class TrainingSession(models.Model):
    """
    Live training sessions and workshops.
    MongoDB-compatible with djongo.
    """
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    course_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to Course")
    instructor_id = models.CharField(max_length=24, blank=True, null=True, help_text="ObjectId reference to instructor User")
    
    # Schedule
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, help_text="Physical location or online meeting link")
    
    # Capacity and enrollment
    max_participants = models.PositiveIntegerField()
    participant_ids = djongo_models.JSONField(default=list, blank=True, help_text="List of ObjectIds for participants")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Materials
    session_materials = models.FileField(upload_to='session_materials/', blank=True, null=True)
    recording_link = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Training Session'
        verbose_name_plural = 'Training Sessions'
        ordering = ['-start_datetime']
    
    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
    
    def get_course(self):
        """Helper method to get the associated course"""
        if self.course_id:
            try:
                return Course.objects.get(id=self.course_id)
            except Course.DoesNotExist:
                return None
        return None
    
    def get_instructor(self):
        """Helper method to get the instructor"""
        if self.instructor_id:
            try:
                from accounts.models import User
                return User.objects.get(id=self.instructor_id)
            except User.DoesNotExist:
                return None
        return None
    
    def get_participants(self):
        """Helper method to get participants"""
        if self.participant_ids:
            try:
                from accounts.models import User
                return User.objects.filter(id__in=self.participant_ids)
            except:
                return []
        return []
    
    @property
    def participant_count(self):
        """Get current participant count"""
        return len(self.participant_ids) if self.participant_ids else 0
    
    @property
    def is_full(self):
        """Check if session is at capacity"""
        return self.participant_count >= self.max_participants


class SessionAttendance(models.Model):
    """
    Attendance tracking for training sessions.
    MongoDB-compatible with djongo.
    """
    
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('absent', 'Absent'),
        ('cancelled', 'Cancelled'),
    ]
    
    session_id = models.CharField(max_length=24, help_text="ObjectId reference to TrainingSession")
    user_id = models.CharField(max_length=24, help_text="ObjectId reference to User")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    # Feedback
    rating = models.PositiveIntegerField(null=True, blank=True, help_text="Session rating out of 5")
    feedback = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Session Attendance'
        verbose_name_plural = 'Session Attendance'
    
    def __str__(self):
        user = self.get_user()
        session = self.get_session()
        user_name = user.get_full_name() if user else "Unknown User"
        session_title = session.title if session else "Unknown Session"
        return f"{user_name} - {session_title} ({self.status})"
    
    def get_session(self):
        """Helper method to get the training session"""
        try:
            return TrainingSession.objects.get(id=self.session_id)
        except TrainingSession.DoesNotExist:
            return None
    
    def get_user(self):
        """Helper method to get the user"""
        try:
            from accounts.models import User
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return None
