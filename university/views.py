from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from university.models import Curs, Lesson, Paying, Subscription
from university.serializer import CursSerializers, LessonSerializers, PayingSerializers, SubscriptionSerializers
from rest_framework.permissions import IsAuthenticated
from university.permissions import OwnerOrAdmin, OwnerOrStaffOrAdmin, OwnerOrStafOrAdminView, OwnerOrAdminChange, \
    OwnerOrAdminChangeSubscribe
from rest_framework.pagination import PageNumberPagination

from university.services.mailing import send_email
from user_auth.models import User


# Create your views here.



class PaginationClass(PageNumberPagination):
    page_size = 2  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр запроса для указания количества элементов на странице
    max_page_size = 10  # Максимальное количество элементов на странице


class CursViewSet(viewsets.ModelViewSet):
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
    permission_classes = [OwnerOrAdminChange]
    serializer_class = CursSerializers
    queryset = Curs.objects.all()
    pagination_class = PaginationClass

    def get(self, request):
        queryset = Curs.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CursSerializers(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
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
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    pagination_class = PaginationClass

    def get(self, request):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializers(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            # Пользователь с правами персонала или администратора может видеть все уроки
            queryset = queryset.order_by('title')
        else:
            # Обычный пользователь - только свои
            queryset = queryset.filter(owner=self.request.user).order_by('title')
        return queryset


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [OwnerOrStaffOrAdmin, IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

class LessonUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [OwnerOrAdmin, IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [OwnerOrAdmin, IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()


class PayingViewSet(viewsets.ModelViewSet):
    permission_classes = [OwnerOrStaffOrAdmin, IsAuthenticated]
    serializer_class = PayingSerializers
    queryset = Paying.objects.all()


class PayingListAPIView(generics.ListAPIView):
    """сортировка    по    дате    оплаты и по сумме
    localhost:8000/university/payings/?ordering=-date_pay
    localhost:8000/university/payings/?ordering=amount

    фильтрация     по    курсу    или    уроку,
    localhost:8000/university/payings/?paid_for_curs=1
    localhost:8000/university/payings/?paid_for_lesson=2

    фильтрация    по    способу    оплаты.
    localhost:8000/university/payings/?payment_method=cash
    localhost:8000/university/payings/?payment_method=transfer
    """
    permission_classes = [OwnerOrStaffOrAdmin, IsAuthenticated]
    queryset = Paying.objects.all()
    serializer_class = PayingSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['paid_for_curs', 'paid_for_lesson', 'payment_method']
    ordering_fields = ['date_pay', 'amount']

class SubscriptionCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user, curs_id=self.request.data['curs'])


    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
    #     data['user'] = request.user.id
    #     data['curs'] = kwargs['curs_id']
    #
    #     mutable_request = request._mutable
    #     request._mutable = True
    #     request.data = data
    #
    #     response = super().create(request, *args, **kwargs)
    #
    #     request._mutable = mutable_request
    #
    #     return response

    # def create(self, request, *args, **kwargs):
    #     request.data['user'] = self.request.user.id
    #     return super().create(request, *args, **kwargs)
        #, status=status.HTTP_201_CREATED, headers=headers)

    # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class SubscriptionAPIView(generics.RetrieveAPIView):
    permission_classes = [OwnerOrStafOrAdminView, IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()

class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [OwnerOrAdminChangeSubscribe, IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()

class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [OwnerOrAdminChangeSubscribe, IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()

class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [OwnerOrAdminChangeSubscribe, IsAuthenticated]
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()

class SubscriptionListView(generics.ListAPIView):
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
        if self.request.user.is_staff or self.request.user.is_superuser:
            # Пользователь с правами персонала или администратора может видеть все подписки
            queryset = queryset.order_by('user')
        else:
            # Обычный пользователь - только свои
            queryset = queryset.filter(owner=self.request.user).order_by('user')
        return queryset



