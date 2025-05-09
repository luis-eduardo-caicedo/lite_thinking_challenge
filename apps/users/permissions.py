from rest_framework.permissions import BasePermission


class IsAdministrator(BasePermission):
    """
    Allows access only to users with is_admin=True.
    """
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.is_admin



class IsExternalUser(BasePermission):
    """
    Allows access only to users with is_admin=False.
    """
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return not user.is_admin
