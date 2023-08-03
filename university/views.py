from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response

from university.models import Curs, Lesson, Subscription
from university.serializer import CursSerializers, LessonSerializers, SubscriptionSerializers
from rest_framework.permissions import IsAuthenticated
from university.permissions import OwnerOrAdmin, OwnerOrStaffOrAdmin, OwnerOrStafOrAdminView, OwnerOrAdminChange, \
    OwnerOrAdminChangeSubscribe
from university.paginations import PaginationClass

from university.services.mailing import send_email
from user_auth.models import User


# Create your views here.

"""
university/ ^curs/$ [name='curs-list']
university/ ^curs\.(?P<format>[a-z0-9]+)/?$ [name='curs-list']
university/ ^curs/(?P<pk>[^/.]+)/$ [name='curs-detail']
university/ ^curs/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='curs-detail']

- Для создания нового объекта `Curs`:
  POST /curs/
- Для обновления существующего объекта `Curs`:
  PUT /curs/<id>/
  PATCH /curs/<id>/
- Для удаления существующего объекта `Curs`:
   DELETE /curs/<id>/
- Для вывода списка всех объектов `Curs`:
    GET /curs/
"""
class CursViewSet(viewsets.ModelViewSet):
    """
    Viewset for curs
    """
    permission_classes = [OwnerOrAdminChange]
    serializer_class = CursSerializers
    queryset = Curs.objects.all()
    pagination_class = PaginationClass


    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=CursSerializers)
        }
    )

    def get(self, request):
        queryset = Curs.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CursSerializers(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Curs.objects.none()
        if not self.request.user.is_authenticated:
            # неавторизованный пользователь- ничего не возвращаем
            return Curs.objects.none()
        else:
            if self.request.user.is_staff or self.request.user.is_superuser:
                # Пользователь с правами персонала или администратора может видеть все курсы
                queryset = queryset.order_by('title')
            else:
                # Обычный пользователь - только свои
                queryset = queryset.filter(owner=self.request.user).order_by('title')
            return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Получаем список пользователей, подписанных на данный курс
        subscribed_users = Subscription.objects.filter(curs=instance).values_list('user', flat=True)

        # Отправляем уведомление по электронной почте каждому пользователю
        message_body = f'Обновление курса.\nКурс "{instance.title}" был обновлен. Проверьте новые материалы.'
        subject = 'Обновление курса'
        for user_id in subscribed_users:
            if request.user:
                user = User.objects.get(id=user_id)
                email = user.email
                send_email(subject, message_body, email)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Получаем список пользователей, подписанных на данный курс
        # subscribed_users = Subscription.objects.filter(curs=instance, subscribed=True).values_list('user', flat=True)
        subscribed_users = Subscription.objects.filter(curs=instance).values_list('user', flat=True)
        # Отправляем уведомление по электронной почте каждому пользователю
        message_body = f'Обновление курса.\nКурс "{instance.title}" был обновлен. Проверьте новые материалы.'
        subject = 'Обновление курса'
        for user_id in subscribed_users:
            user = User.objects.get(id=user_id)
            email = user.email
            send_email(subject, message_body, email)
        return Response(serializer.data)


class LessonListView(generics.ListAPIView):
    """
    list view lesson
    Выводит список уроков. Для просмотра требуется авторизация.
    Администратор или менеджер могут просматривать все уроки, обычный
    пользователь - только свои.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    pagination_class = PaginationClass

    @swagger_auto_schema(
        responses={200: openapi.Response(description='Success', schema=LessonSerializers)},
    )

    def get(self, request):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializers(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=LessonSerializers)
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Lesson.objects.none()
        if not self.request.user.is_authenticated:
            return Lesson.objects.none()
        else:
            if self.request.user.is_staff or self.request.user.is_superuser:
                # Пользователь с правами персонала или администратора может видеть все уроки
                queryset = queryset.order_by('title')
            else:
                # Обычный пользователь - только свои
                queryset = queryset.filter(owner=self.request.user).order_by('title')
            return queryset


class LessonCreateAPIView(generics.CreateAPIView):
    """
    create view lesson
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Lesson.objects.none()
        else:
            return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    retrieve view lesson
    """
    permission_classes = [OwnerOrStaffOrAdmin, IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Lesson.objects.none()
        else:
            return queryset

class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    update view lesson
    """
    permission_classes = [OwnerOrAdmin, IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Lesson.objects.none()
        else:
            return queryset


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    destroy view lesson
    """
    permission_classes = [OwnerOrAdmin, IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Lesson.objects.none()
        else:
            return queryset

class SubscriptionCreateAPIView(generics.CreateAPIView):
    """
    create view subscription
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Subscription.objects.none()
        else:
            return queryset


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """
    update view subscription
    """
    permission_classes = [OwnerOrAdminChangeSubscribe, IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Subscription.objects.none()
        else:
            return queryset

class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """
    destroy view subscription
    """
    permission_classes = [OwnerOrAdminChangeSubscribe, IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Subscription.objects.none()
        else:
            return queryset

class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    """
    retrieve view subscription
    """
    permission_classes = [OwnerOrAdminChangeSubscribe, IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Subscription.objects.none()
        else:
            return queryset


class SubscriptionListView(generics.ListAPIView):
    """
    list view subscription
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()
    pagination_class = PaginationClass

    def get(self, request):
        queryset = Subscription.objects.all().order_by('user')
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializers(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if not self.request:
            return Subscription.objects.none()
        if not self.request.user.is_authenticated:
            return Subscription.objects.none()
        else:
            if self.request.user.is_staff or self.request.user.is_superuser:
                # Пользователь с правами персонала или администратора может видеть все подписки
                queryset = queryset.order_by('user')
            else:
                # Обычный пользователь - только свои
                queryset = queryset.filter(owner=self.request.user).order_by('user')

        return queryset

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=SubscriptionSerializers)
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)








