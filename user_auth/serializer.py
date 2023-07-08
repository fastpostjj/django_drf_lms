from rest_framework import serializers
from django.db import models
from user_auth.models import User

class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'avatar',
            'country',
                )

