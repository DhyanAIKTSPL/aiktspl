"""
Authentication and user management API views.
"""

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.utils import timezone
from django.db.models import Q

from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    UserProfileDetailSerializer,
    PasswordChangeSerializer,
    UserApprovalSerializer,
    PendingUsersSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint with role-based approval workflow.
    """
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create new user and return appropriate response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Prepare response based on approval status
        if user.is_approved:
            message = "Registration successful! You can now log in."
        else:
            message = "Registration successful! Your account is pending admin approval."
        
        return Response({
            'message': message,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'is_approved': user.is_approved,
            }
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login endpoint with approval check and user data.
    """
    
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(generics.GenericAPIView):
    """
    Logout endpoint that blacklists the refresh token.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Logout user and blacklist refresh token"""
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    User profile view and update endpoint.
    """
    
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Return current user's profile"""
        return self.request.user


class PasswordChangeView(generics.GenericAPIView):
    """
    Password change endpoint for authenticated users.
    """
    
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Change user password"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Update password
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


class PendingUsersView(generics.ListAPIView):
    """
    List users pending approval (Admin only).
    """
    
    serializer_class = PendingUsersSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return pending users for admin users only"""
        if not self.request.user.is_admin:
            return User.objects.none()
        
        return User.objects.filter(is_approved=False).order_by('date_joined')


class ApproveUserView(generics.UpdateAPIView):
    """
    Approve user endpoint (Admin only).
    """
    
    serializer_class = UserApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return users for admin users only"""
        if not self.request.user.is_admin:
            return User.objects.none()
        
        return User.objects.all()
    
    def update(self, request, *args, **kwargs):
        """Approve or disapprove user"""
        user = self.get_object()
        action = request.data.get('action')  # 'approve' or 'disapprove'
        
        if action == 'approve':
            user.approve_user(request.user)
            message = f"User {user.get_full_name()} has been approved"
        elif action == 'disapprove':
            user.is_approved = False
            user.approved_by = None
            user.approved_at = None
            user.save()
            message = f"User {user.get_full_name()} has been disapproved"
        else:
            return Response({
                'error': 'Invalid action. Use "approve" or "disapprove"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': message,
            'user': self.get_serializer(user).data
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user information.
    """
    
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    Get user statistics for dashboard.
    """
    
    user = request.user
    
    # Basic stats available to all users
    stats = {
        'profile_completion': 0,
        'account_status': 'approved' if user.is_approved else 'pending',
        'role': user.role,
        'member_since': user.date_joined.strftime('%B %Y'),
    }
    
    # Calculate profile completion percentage
    profile_fields = [
        user.first_name, user.last_name, user.email, user.phone,
        user.department, user.position, user.bio
    ]
    completed_fields = sum(1 for field in profile_fields if field)
    stats['profile_completion'] = int((completed_fields / len(profile_fields)) * 100)
    
    # Role-specific stats
    if user.is_admin:
        stats.update({
            'pending_approvals': User.objects.filter(is_approved=False).count(),
            'total_employees': User.objects.filter(role__in=['employee', 'trainee']).count(),
            'active_projects': 0,  # Will be updated when project APIs are added
        })
    
    elif user.is_employee or user.is_trainee:
        stats.update({
            'active_tasks': 0,  # Will be updated when task APIs are added
            'completed_tasks': 0,
            'attendance_rate': 0,  # Will be updated when attendance APIs are added
        })
    
    return Response(stats)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_profile_picture(request):
    """
    Update user profile picture.
    """
    
    if 'profile_picture' not in request.FILES:
        return Response({
            'error': 'No profile picture provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    user.profile_picture = request.FILES['profile_picture']
    user.save()
    
    return Response({
        'message': 'Profile picture updated successfully',
        'profile_picture_url': user.profile_picture.url if user.profile_picture else None
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_users(request):
    """
    Search users by name, email, or employee ID.
    """
    
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({'results': []})
    
    # Basic search available to all users
    users = User.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query) |
        Q(employee_id__icontains=query),
        is_approved=True
    ).select_related('profile')[:10]
    
    results = []
    for user in users:
        results.append({
            'id': user.id,
            'name': user.get_full_name(),
            'email': user.email,
            'role': user.role,
            'department': user.department,
            'employee_id': user.employee_id,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
        })
    
    return Response({'results': results})
