from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters
from rest_framework.generics import get_object_or_404

from university.models import Curs, Lesson, Paying
from university.serializer import CursSerializers, LessonSerializers, PayingSerializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from university.permissions import OwnerOrAdmin, OwnerOrStaffOrAdmin, OwnerOrStafOrOrAdminView, OwnerOrOrAdminChange

# Create your views here.


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
    permission_classes = [OwnerOrOrAdminChange]
    serializer_class = CursSerializers
    queryset = Curs.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.is_superuser:
            # Пользователь с правами персонала или администратора может видеть все курсы
            queryset = queryset.order_by('title')
        else:
            # Обычный пользователь - только свои
            queryset = queryset.filter(owner=self.request.user).order_by('title')
        return queryset


class LessonListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [OwnerOrStaffOrAdmin, IsAuthenticated]
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

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

