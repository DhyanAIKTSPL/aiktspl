"""
Serializers for user authentication and profile management.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with role-based approval.
    """
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone',
            'role', 'password', 'password_confirm', 'department', 'position'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        """Validate password confirmation and email uniqueness"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("User with this email already exists")
        
        return attrs
    
    def create(self, validated_data):
        """Create new user with approval workflow"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        # Auto-approve admins, others need approval
        validated_data['is_approved'] = validated_data.get('role') == 'admin'
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer with user approval check.
    """
    
    def validate(self, attrs):
        """Validate credentials and check approval status"""
        # Use email as username for authentication
        email = attrs.get('username')  # DRF uses 'username' field name
        password = attrs.get('password')
        
        if email and password:
            # Try to find user by email
            try:
                user = User.objects.get(email=email)
                attrs['username'] = user.username  # Set actual username for parent validation
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials')
        
        # Call parent validation
        data = super().validate(attrs)
        
        # Check if user is approved
        if not self.user.is_approved:
            raise serializers.ValidationError(
                'Your account is pending admin approval. Please contact your administrator.'
            )
        
        # Add user data to response
        data.update({
            'user': {
                'id': self.user.id,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'role': self.user.role,
                'is_approved': self.user.is_approved,
                'employee_id': self.user.employee_id,
                'department': self.user.department,
                'position': self.user.position,
            }
        })
        
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    """
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_employee = serializers.BooleanField(read_only=True)
    is_trainee = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'role', 'is_approved', 'employee_id', 'department', 'position',
            'hire_date', 'salary', 'profile_picture', 'bio', 'date_of_birth', 'address',
            'is_admin', 'is_employee', 'is_trainee', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'username', 'role', 'is_approved', 'date_joined', 'last_login']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer including extended profile information.
    """
    
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'role', 'is_approved', 'employee_id', 'department', 'position',
            'hire_date', 'salary', 'profile_picture', 'bio', 'date_of_birth', 'address',
            'date_joined', 'last_login', 'profile'
        ]
        read_only_fields = ['id', 'username', 'role', 'is_approved', 'date_joined', 'last_login']
    
    def get_profile(self, obj):
        """Get extended profile information"""
        try:
            profile = obj.profile
            return {
                'emergency_contact_name': profile.emergency_contact_name,
                'emergency_contact_phone': profile.emergency_contact_phone,
                'emergency_contact_relationship': profile.emergency_contact_relationship,
                'skills': profile.skills,
                'certifications': profile.certifications,
                'linkedin_url': profile.linkedin_url,
                'github_url': profile.github_url,
                'theme_preference': profile.theme_preference,
                'notification_preferences': profile.notification_preferences,
            }
        except UserProfile.DoesNotExist:
            return None


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change functionality.
    """
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validate old password and new password confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        
        return attrs
    
    def validate_old_password(self, value):
        """Validate old password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value


class UserApprovalSerializer(serializers.ModelSerializer):
    """
    Serializer for admin user approval actions.
    """
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'is_approved', 'approved_at']
        read_only_fields = ['id', 'email', 'first_name', 'last_name', 'role', 'approved_at']


class PendingUsersSerializer(serializers.ModelSerializer):
    """
    Serializer for listing pending user approvals.
    """
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    days_pending = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'role', 'department', 'position',
            'date_joined', 'days_pending'
        ]
    
    def get_days_pending(self, obj):
        """Calculate days since registration"""
        from django.utils import timezone
        return (timezone.now() - obj.date_joined).days
