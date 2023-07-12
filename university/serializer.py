from rest_framework import serializers
from django.db import models
from university.models import Curs, Lesson, Paying

class CursSerializers(serializers.ModelSerializer):
    "Для сериализатора для модели курса реализуйте поле вывода уроков."
    lessons_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Curs
        fields = (
            'id',
            'title',
            'preview',
            'description',
            'lessons_count',
            'lessons',
        )
    def get_lessons_count(self,  obj):
        # return Lesson.objects.filter(pk=id_curs).count()
        return obj.lesson_set.count()

    def get_lessons(self, obj):
        lesson_serializers = LessonSerializers(obj.lesson_set.all(), many=True)
        return lesson_serializers.data

class LessonSerializers(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            'title',
            'preview',
            'description',
            'url_video',
            'curs',
        )

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


