from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from vdoc_api.models import Consultant

User = get_user_model()


class UserPermissions(BasePermission):
    SAFE_METHODS = ['POST']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS or request.user and request.user.is_authenticated \
                or request.user and request.user.is_authenticated and Consultant.objects.filter(user=request.user):
            return True
        return False


class ConsultantPermissions(BasePermission):
    SAFE_METHODS = ['POST']

    def has_permission(self, request, view):
        if request.method in self.SAFE_METHODS or request.user and request.user.is_authenticated \
                and Consultant.objects.filter(user=request.user):
            return True
        return False


class QuestionSetPermissions(BasePermission):
    SAFE_METHODS = []

    def has_permission(self, request, view):
        allow = False
        if request.method in self.SAFE_METHODS:
            allow = True

        if request.user and request.user.is_authenticated and \
                (
                        Consultant.objects.filter(user=request.user) or
                        (
                                User.objects.filter(id=request.user.id, code__isnull=False).exclude(code="")
                                and request.method == "GET"
                        )
                ):
            allow = True
        return allow


class QuestionPermissions(QuestionSetPermissions):
    SAFE_METHODS = []


class AnswerPermissions(QuestionPermissions):
    SAFE_METHODS = []

    def has_permission(self, request, view):
        allow = False
        if request.method in self.SAFE_METHODS:
            allow = True

        if request.user and request.user.is_authenticated and \
                (

                            User.objects.filter(id=request.user.id, code__isnull=False)
                            and request.method == "POST"
                ):
            allow = True
        return allow