from rest_framework.permissions import BasePermission

from university.models import Lesson, Curs, Subscription


class OwnerOrStaffOrAdmin(BasePermission):
    # проверка для уроков

    def has_permission(self, request, view):
        if request.method == 'GET':
            # для списка не проверяем владельца
            if request.user.is_staff or request.user.is_superuser:
                return True
            elif 'pk' in view.kwargs:
                # это не список
                lesson_id = view.kwargs['pk']
                lesson = Lesson.objects.get(id=lesson_id)
                if request.user == lesson.owner:
                    return True
        return False


class OwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True
        elif request.user.is_superuser:
            return True
        return False

class OwnerOrStafOrAdminView(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        elif request.user.is_staff:
            return True
        elif request.user.is_superuser:
            return True
        return False


class OwnerOrAdminChange(BasePermission):
    # для вьюсета для объектов курса
    def has_object_permission(self, request, view, obj):
        if request.method.upper() == 'POST':
            if request.user:
                return True
        elif request.method.upper() in ['PUT', 'PATCH', 'DELETE']:
            if request.user == obj.owner:
                return True
            elif request.user.is_superuser:
                return True
        elif request.method.upper() == 'GET':
            # для списка не проверяем владельца
            if request.user.is_staff or request.user.is_superuser:
                return True
            elif 'pk' in view.kwargs:
                # это не список
                curs_id = view.kwargs['pk']
                curs = Curs.objects.get(id=curs_id)
                if request.user == curs.owner:
                    return True
        return False

class OwnerOrAdminChangeSubscribe(BasePermission):
    # для вьюсета для объектов подписки
    def has_object_permission(self, request, view, obj):
        if request.method.upper() == 'POST':
            if request.user:
                return True
        elif request.method.upper() in ['PUT', 'PATCH', 'DELETE']:
            if request.user == obj.user:
                return True
            elif request.user.is_superuser:
                return True
        elif request.method.upper() == 'GET':
            # для списка не проверяем владельца
            if request.user.is_staff or request.user.is_superuser:
                return True
            elif 'pk' in view.kwargs:
                # это не список
                sub_id = view.kwargs['pk']
                subs = Subscription.objects.get(id=sub_id)
                if request.user == subs.user:
                    return True
        return False


