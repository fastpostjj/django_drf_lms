import requests
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, filters, viewsets, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.models import Paying
from payments.serializer import PayingSerializers, PayingSerializers_create_payment_for_curs, \
    PayingSerializers_create_payment_methods, PayingSerializers_confirm_payment
from university.models import Curs, Lesson
from university.permissions import OwnerOrStaffOrAdmin
from user_auth.models import User
from payments.services.payment import StripePay, StripePaymentMethod
from user_auth.serializer import UsersSerializers

# Create your views here.


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
class PayingListAPIView(generics.ListAPIView):
    """
    list view paying
    """
    permission_classes = [OwnerOrStaffOrAdmin, IsAuthenticated]
    queryset = Paying.objects.all()
    serializer_class = PayingSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['paid_for_curs', 'paid_for_lesson', 'payment_method']
    ordering_fields = ['date_pay', 'amount']

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Paying.objects.none()
        else:
            return queryset

class PayingViewSet(viewsets.ModelViewSet):
    """
     paying viewset
    """
    permission_classes = [OwnerOrStaffOrAdmin, IsAuthenticated]
    serializer_class = PayingSerializers
    queryset = Paying.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Paying.objects.none()
        else:
            return queryset

class PayingMethodCreateAPIView(generics.UpdateAPIView):
    """
    view create payment method for current user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PayingSerializers_create_payment_methods
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Paying.objects.none()
        else:
            return queryset

    def update(self, request, *args, **kwargs):
        payment_method = StripePay()
        payment_method_created = payment_method.create_payment_method()

        if payment_method_created:
            id = payment_method.payment_method_id

            # Привязываем платежный метод к пользователю
            user = request.user
            user.id_payment_method = id
            user.save()

            serializer = self.get_serializer(user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response({"error": "Ошибка создания платежного метода"}, status=status.HTTP_400_BAD_REQUEST)


class PayingCreateAPIView(generics.CreateAPIView):
    """
    view create payment intent for paying for curs or lesson
    """
    permission_classes = [IsAuthenticated]
    queryset = Paying.objects.all()
    serializer_class = PayingSerializers_create_payment_for_curs

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Paying.objects.none()
        else:
            return queryset

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        amount = self.request.data.get('amount')
        id_curs = self.request.data.get('curs')
        id_lesson = self.request.data.get('lesson')
        curs = None
        lesson = None
        if id_curs:
            if Curs.objects.filter(pk=int(id_curs)).exists():
                curs = Curs.objects.filter(pk=int(id_curs))[0]
                # оплата за курс
                description = 'Оплата за курс'
                amount = curs.amount
                metadata = {
                            'paid_for_curs': id_curs,
                        }
            else:
                raise serializers.ValidationError(f"Курс с id={id_curs} не существует")
        else:
            if Lesson.objects.filter(pk=int(id_lesson)).exists():
                lesson = Lesson.objects.filter(pk=int(id_lesson))[0]
                amount = lesson.amount
                # оплата за курс
                description = 'Оплата за урок'
                metadata = {
                            'paid_for_lesson': id_lesson,
                        }
            else:
                raise serializers.ValidationError(f"Урок с id={id_lesson} не существует")



        print('amount=',amount, ', id_curs=', id_curs," id_lesson=",id_lesson)

        stripe_pay = StripePay()
        # Создание платежного намерения
        stripe_pay.create_intent(
            amount=amount,
            currency='rub',
            description=description,
            payment_method_types='card',
            metadata=metadata
        )

        serializer.save(
            user=self.request.user,
            amount=amount,
            paid_for_curs=curs,
            paid_for_lesson=lesson,
            payment_method='card',
            id_intent=stripe_pay.payment_intent_id,
            status=stripe_pay.status
        )
        payment_serializer = PayingSerializers()
        return Response(payment_serializer.data, status=status.HTTP_201_CREATED)

class PayingConfirmCreateAPIView(generics.CreateAPIView):
    """
    view confirm payment for current user
    """
    permission_classes = [IsAuthenticated]
    queryset = Paying.objects.all()
    serializer_class = PayingSerializers_confirm_payment

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description='Success', schema=PayingSerializers_confirm_payment)
        }
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            # user = serializer.validated_data['user'] # вариант брать пользователя из отправленных данных
            user = request.user
            id = serializer.validated_data['id']
            try:
                paying = Paying.objects.get(pk=int(id))
            except Paying.DoesNotExist:
                raise serializers.ValidationError(f"Нет платежа с id={id}")
            id_intent = paying.id_intent
            # print("user.id_payment_method=", user.id_payment_method, ", id_intent=",id_intent)
            if id_intent is None or id_intent == "":
                raise serializers.ValidationError(f"Платежное намерение не передано")
            if user.id_payment_method is None or user.id_payment_method == "":
                raise serializers.ValidationError(f"У пользователя {user} не задан платежный метод {user.id_payment_method}")

            try:
                stripe_pay = StripePay()
                stripe_pay.confirm_payment(id_intent, user.id_payment_method)
                payment_serializer = PayingSerializers()
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)

            except Exception as error:
                raise serializers.ValidationError(f"Ошибка подтверждения платежа: {error}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self, *args, **kwargs):
        # Для совместимости с автодокументацией
        queryset = super().get_queryset()
        if not self.request:
            return Paying.objects.none()
        else:
            return queryset







