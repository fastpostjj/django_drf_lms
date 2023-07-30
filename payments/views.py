from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, viewsets
from rest_framework.permissions import IsAuthenticated

from payments.models import Paying
from payments.serializer import PayingSerializers
from university.permissions import OwnerOrStaffOrAdmin

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

class PayingViewSet(viewsets.ModelViewSet):
    """
     paying viewset
    """
    permission_classes = [OwnerOrStaffOrAdmin, IsAuthenticated]
    serializer_class = PayingSerializers
    queryset = Paying.objects.all()
