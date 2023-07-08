from rest_framework import serializers
from django.db import models
from university.models import Curs, Lesson

class CursSerializers(serializers.ModelSerializer):
    class Meta:
        model = Curs
        fields = (
            'title',
            'preview',
            'description',
        )

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


