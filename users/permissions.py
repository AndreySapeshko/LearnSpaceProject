from rest_framework.permissions import BasePermission

from courses.models import Course, Lesson


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderators').exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if isinstance(obj, Course):
            return obj.user == request.user
        else:
            return obj.course.user == request.user
