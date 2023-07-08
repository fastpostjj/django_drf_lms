from django.db import models
from config.settings import NULLABLE

# Create your models here.
'''
Создайте модели пользователя, курса и урока.
Описать CRUD для модели курса через Viewsets и для урока через Generic-классы.
Описать простейшие сериализаторы для работы контроллеров.
'''

# class User(models.Model):
"""
    Пользователь:
    все поля от обычного пользователя, но авторизацию заменить на email
    телефон
    город
    аватарка
    """

class Curs(models.Model):
    """
    название
    превью (картинка)
    описание
    title
    preview
    description
    """
    title = models.CharField(max_length=128, verbose_name='курс')
    preview = models.ImageField(verbose_name="Превью курса", upload_to="university/curs/", **NULLABLE)
    description = models.TextField( verbose_name='Описание курса', **NULLABLE)

    def __str__(self):
        return f'Курс {self.title} '

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

class Lesson(models.Model):
    """
    Урок:
    название
    описание
    превью (картинка)
    ссылка на видео
    title
    description
    preview
    url_video
    curs
    """
    title = models.CharField(max_length=128, verbose_name='урок')
    description = models.TextField( verbose_name='Описание урока', **NULLABLE)
    preview = models.ImageField(verbose_name="Превью урока", upload_to="university/lessons/", **NULLABLE)
    url_video = models.URLField(verbose_name="ссылка на видео", **NULLABLE)
    curs = models.ForeignKey(Curs,
                             verbose_name='курс',
                             on_delete=models.SET_NULL,
                             **NULLABLE)

    def __str__(self):
        return f'Урок {self.title}, курс {self.curs} '

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

