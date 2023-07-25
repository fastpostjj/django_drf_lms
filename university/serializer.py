from rest_framework import serializers
from django.db import models
from university.models import Curs, Lesson, Paying, Subscription

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
                # 'user',
                'curs',
                # 'subscribed',
        )

class CursSerializers(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField(read_only=True)
    # milage = MilageSerializer(many=True, read_only=True, source='milage_set')
    # subscribed = SubscriptionSerializers(read_only=True, source='subscription_set')

    class Meta:
        model = Curs
        fields = (
            # 'id',
            'title',
            'preview',
            'description',
            'lessons_count',
            'lessons',
            'owner',
            # 'is_subscribed',
            # 'subscribed',
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
            # subscribed = Subscription.objects.filter(user=user, curs=obj).exists()
            subscribed = SubscriptionSerializers(obj.suscription_set.all(), many=True)
                # user=user, curs=obj).exists()
            return subscribed
        return False
            # is_subscribed = SubscriptionSerializers(obj.subscription_set.all())


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

class PayingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Paying
        fields = (
            'user',
            'date_pay',
            'paid_for_curs',
            'paid_for_lesson',
            'amount',
            'payment_method',
        )



