from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters
from university.models import Curs, Lesson, Paying
from university.serializer import CursSerializers, LessonSerializers, PayingSerializers

# Create your views here.
class CursViewSet(viewsets.ModelViewSet):
    serializer_class = CursSerializers
    queryset = Curs.objects.all()


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()

class PayingViewSet(viewsets.ModelViewSet):
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
    queryset = Paying.objects.all()
    serializer_class = PayingSerializers
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['paid_for_curs', 'paid_for_lesson', 'payment_method']
    ordering_fields = ['date_pay', 'amount']

