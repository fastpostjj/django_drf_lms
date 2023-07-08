from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


# Create your models here.

class User(AbstractUser):
    """
    все поля от обычного пользователя, но авторизацию заменить на email
    телефон
    город
    аватарка
    email
    phone
    avatar
    country
    """

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users_auth/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=150, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

