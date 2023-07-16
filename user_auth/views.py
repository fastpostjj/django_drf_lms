from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import render
from rest_framework import viewsets

from user_auth.models import User
from user_auth.serializer import UsersSerializers, MyTokenObtainPairSerializer


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializers
    queryset = User.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
# представление (view) для получения JWT-токена.
    serializer_class = MyTokenObtainPairSerializer


