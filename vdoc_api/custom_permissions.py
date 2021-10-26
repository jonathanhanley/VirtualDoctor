from rest_framework.permissions import BasePermission

from vdoc_api.models import Consultant


class UserPermissions(BasePermission):
    SAFE_METHODS = ['POST']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS or request.user and request.user.is_authenticated:
            return True
        return False


class ConsultantPermissions(BasePermission):
    SAFE_METHODS = ['POST']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS or request.user and request.user.is_authenticated\
                and Consultant.objects.filter(user=request.user):
            return True
        return False
