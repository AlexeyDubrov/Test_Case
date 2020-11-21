from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class AnonymousUserIsSetIdentifier(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

        identifier = request.GET.get('identifier')

        if not identifier:
            raise PermissionDenied(
                    detail='Please add AnonymousUserID to URL parameters',
                    code=410)

        return True
