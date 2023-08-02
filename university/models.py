from django.db import models

from config import settings
from config.settings import NULLABLE
from user_auth.models import User

# Create your models here.
class Curs(models.Model):
    """
    название
    превью (картинка)
    описание
    title
    preview
    description
    owner
    """
    title = models.CharField(max_length=128,
                             verbose_name='курс')
    preview = models.ImageField(verbose_name="Превью курса",
                                upload_to="university/curs/",
                                **NULLABLE)
    description = models.TextField( verbose_name='Описание курса',
                                    **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name='владелец',
                              on_delete=models.SET_NULL,
                              **NULLABLE)
    amount = models.FloatField(verbose_name="Цена курса, руб.", **NULLABLE)

    def __str__(self):
        return f'{self.title} '

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
    owner
    """
    title = models.CharField(max_length=128,
                             verbose_name='урок')
    description = models.TextField( verbose_name='Описание урока',
                                    **NULLABLE)
    preview = models.ImageField(verbose_name="Превью урока",
                                upload_to="university/lessons/",
                                **NULLABLE)
    url_video = models.URLField(verbose_name="ссылка на видео",
                                **NULLABLE)
    curs = models.ForeignKey(Curs,
                             verbose_name='курс',
                             on_delete=models.SET_NULL,
                             **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name='владелец',
                              on_delete=models.SET_NULL,
                              **NULLABLE)
    amount = models.FloatField(verbose_name="Цена урока, руб.", **NULLABLE)

    def __str__(self):
        return f'Урок {self.title}, курс {self.curs} '

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

class Subscription(models.Model):
    """
    Подписка на обновления курса для пользователя
    user
    curs
    subscribed
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    curs = models.ForeignKey(Curs, on_delete=models.CASCADE)
    # subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f'Подписка {self.user}, курс "{self.curs}"'

    class Meta:
        unique_together = ('user', 'curs')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

