from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAdminOrReadOnly(BasePermission):
    """Доступ администратора или чтение"""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (not request.user.is_anonymous
                    and request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAuthorOrAdmin(permissions.BasePermission):
    """Доступ для автора или администратора.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (
                request.user == obj.author or request.user.is_admin
                or request.method == 'POST'):
            return True
        return request.method in permissions.SAFE_METHODS
