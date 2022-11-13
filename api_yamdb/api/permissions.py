from rest_framework import permissions
from users.utils import ROLE_TERMS


class AuthorOrAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.role == ROLE_TERMS["admin"]
                or request.user.role == ROLE_TERMS["moderator"]
                or (
                    request.user.role == ROLE_TERMS["user"]
                    and request.user == obj.author
                )
            )
        )


class OnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == ROLE_TERMS["admin"]
                or request.user.is_superuser
            )


class OnlyOwnerAccount(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == ROLE_TERMS["admin"]) or (
                request.method in permissions.SAFE_METHODS
            )
        else:
            return request.method in permissions.SAFE_METHODS
