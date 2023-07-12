from django.urls import path
from rest_framework.routers import DefaultRouter
from university.views import CursViewSet, LessonListView, LessonCreateAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, LessonRetrieveAPIView, PayingViewSet, PayingListAPIView

router = DefaultRouter()
router.register(r'curs', CursViewSet, basename='curs')
router.register(r'payings', PayingViewSet, basename='payings')

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lessons_list'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons_create'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lessons_update'),
    path('lessons/destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='lessons_destroy'),
    path('lessons/retrieve/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessons_retrieve'),
    path('payings/', PayingListAPIView.as_view(), name='payings_list'),
              ] + router.urls
