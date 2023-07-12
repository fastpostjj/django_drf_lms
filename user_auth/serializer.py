from rest_framework import serializers
from django.db import models
from user_auth.models import User
from university.serializer import PayingSerializers

class UsersSerializers(serializers.ModelSerializer):
    paying = PayingSerializers(many=True, read_only=True, source='paying_set')

    class Meta:
        model = User
        fields = (
            'email',
            'country',
            'phone',
            'avatar',
            'paying'
                )


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

