from django.urls import path
from rest_framework.routers import DefaultRouter
from university.views import CursViewSet, LessonListView, LessonCreateAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, LessonRetrieveAPIView, \
    SubscriptionCreateAPIView, SubscriptionListView, SubscriptionUpdateAPIView, SubscriptionDestroyAPIView,\
    SubscriptionRetrieveAPIView

router = DefaultRouter()
router.register(r'curs', CursViewSet, basename='curs')

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lessons_list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons_create'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lessons_update'),
    path('lessons/destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='lessons_destroy'),
    path('lessons/retrieve/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessons_retrieve'),

    path('subscription/', SubscriptionListView.as_view(), name='subscriptions_list'),
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/update/<int:pk>/', SubscriptionUpdateAPIView.as_view(), name='subscription_update'),
    path('subscription/destroy/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_destroy'),
    path('subscription/retrieve/<int:pk>/', SubscriptionRetrieveAPIView.as_view(), name='subscription_retrieve'),

              ] + router.urls
