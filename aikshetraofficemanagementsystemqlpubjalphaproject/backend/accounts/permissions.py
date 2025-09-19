"""
Custom permissions for role-based access control.
"""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission class for admin-only access.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsEmployeeOrAdmin(permissions.BasePermission):
    """
    Permission class for employee and admin access.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['employee', 'admin']
        )


class IsTraineeOrAbove(permissions.BasePermission):
    """
    Permission class for trainee, employee, and admin access.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['trainee', 'employee', 'admin']
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class for resource owner or admin access.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin can access everything
        if request.user.is_admin:
            return True
        
        # Check if user owns the resource
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # For User objects
        if hasattr(obj, 'id') and hasattr(request.user, 'id'):
            return obj.id == request.user.id
        
        return False


class IsManagerOrAdmin(permissions.BasePermission):
    """
    Permission class for managers and admins.
    """
    
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # Admin always has access
        if request.user.is_admin:
            return True
        
        # Check if user is a manager (has managed employees)
        return hasattr(request.user, 'managed_employees') and request.user.managed_employees.exists()


class ReadOnlyOrAdmin(permissions.BasePermission):
    """
    Permission class for read-only access to all, write access to admins.
    """
    
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # Read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for admins
        return request.user.is_admin
