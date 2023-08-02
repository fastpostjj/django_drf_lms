from django.urls import path
from rest_framework.routers import DefaultRouter
from payments.views import  PayingViewSet, PayingListAPIView, PayingCreateAPIView, \
    PayingMethodCreateAPIView, PayingConfirmCreateAPIView

router = DefaultRouter()
router.register(r'payings', PayingViewSet, basename='payings')

urlpatterns = [
    path('payings/', PayingListAPIView.as_view(), name='payings_list'),
    path('paying_methods/create/', PayingMethodCreateAPIView.as_view(), name='paying_methods_create'),
    path('payings/confirm/', PayingConfirmCreateAPIView.as_view(), name='paying_confirm'),
    path('create/', PayingCreateAPIView.as_view(), name='payings_create'),
    ] + router.urls