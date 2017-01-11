from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsAuthenticatedOrCreationOrReadOnly(BasePermission):

    """The request is authenticated as a user and action is create, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            view.action == 'create' or
            request.user and
            request.user.is_authenticated()
        )


class IsSelf(BasePermission):

    """Object-level permission to allow only owner of the object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_suerpuser:
            return True
        else:
            try:
                return obj.token == request.user.token
            except:
                return obj.user == request.user
