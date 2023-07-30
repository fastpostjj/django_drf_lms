from django.urls import path
from rest_framework.routers import DefaultRouter
from payments.views import  PayingViewSet, PayingListAPIView

router = DefaultRouter()
router.register(r'payings', PayingViewSet, basename='payings')

urlpatterns = [
    path('payings/', PayingListAPIView.as_view(), name='payings_list'),
    ] + router.urls