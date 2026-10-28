from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    """Anyone authenticated may read; only the record's creator may modify or delete it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by_id == request.user.id
