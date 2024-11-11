from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    """Class for overridding permissions to verified if user is superuser"""
    def has_permission(self, request, view):
        """superuser rights verification"""
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        """superuser rights verification"""
        return request.user.is_superuser

class IsOwner(permissions.BasePermission):
    """Class for overriding permissions to verified if user is owner of the object"""
    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.username
