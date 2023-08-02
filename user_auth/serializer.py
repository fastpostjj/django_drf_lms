from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db import models
from user_auth.models import User
from payments.serializer import PayingSerializers

class UsersSerializers(serializers.ModelSerializer):
    paying = PayingSerializers(many=True, read_only=True, source='paying_set')

    class Meta:
        model = User
        fields = (
            'email',
            'country',
            'phone',
            'avatar',
            'id_payment_method',
            'paying'
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор  MyTokenObtainPairSerializer  для обработки запросов на получение токена"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token['username'] = user.username
        token['email'] = user.email
        return token


    # def get_paying(self, obj):
    #     # paying_serializers = PayingSerializers(obj.user_set.all(), many=True)
    #     # return paying_serializers.data
    #
    #     paying = obj.paying_set.all()
    #     if paying:
    #         return paying
    #     return []

    # def get_paying(self, obj):
    #     paying_serializers = PayingSerializers(obj.paying_set.all(), many=True)
    #     return paying_serializers.data

