"""
URL patterns for authentication and user management APIs.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile endpoints
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('current-user/', views.current_user, name='current_user'),
    path('user-stats/', views.user_stats, name='user_stats'),
    path('change-password/', views.PasswordChangeView.as_view(), name='change_password'),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    
    # User management (Admin)
    path('pending-users/', views.PendingUsersView.as_view(), name='pending_users'),
    path('approve-user/<int:pk>/', views.ApproveUserView.as_view(), name='approve_user'),
    
    # Search and utilities
    path('search-users/', views.search_users, name='search_users'),
]
