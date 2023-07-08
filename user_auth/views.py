from django.shortcuts import render
from rest_framework import viewsets

from user_auth.models import User
from user_auth.serializer import UsersSerializers


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializers
    queryset = User.objects.all()
