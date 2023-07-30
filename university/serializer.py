from rest_framework import serializers
from django.db import models
from university.models import Curs, Lesson, Subscription

def is_contain_youtube_url(field, value) -> bool:
    if isinstance(value, dict):
        url = value.get(field)
        if url and "youtube" in url:
            return True
    return False
class UrlCustomValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        result = is_contain_youtube_url(
            self.field,
            value
        )
        if not result:
            message = f'Ссылки на сторонние ресурсы не допускаются! Уроки и курсы должны быть размещены на youtube'
            raise serializers.ValidationError(message)


class SubscriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
                'curs',
        )

class CursSerializers(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Curs
        fields = (
            'title',
            'preview',
            'description',
            'lessons_count',
            'is_subscribed',
            'owner',
            'lessons'
        )
    def get_lessons_count(self,  obj):
        return obj.lesson_set.count()

    def get_lessons(self, obj):
        lesson_serializers = LessonSerializers(obj.lesson_set.all(), many=True)
        return lesson_serializers.data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            is_subscribed = Subscription.objects.filter(user=user, curs=obj).exists()
            return is_subscribed
        return False

class LessonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            'title',
            'preview',
            'description',
            'url_video',
            'curs',
            'owner'
        )
        validators = [UrlCustomValidator(field='url_video')]





