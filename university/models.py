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

    def __str__(self):
        return f'Урок {self.title}, курс {self.curs} '

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

class Paying(models.Model):
    """
    Платежи:

    пользователь,
    дата оплаты,
    оплаченный курс или урок,
    сумма оплаты,
    способ оплаты — наличные или перевод на счет.
    user
    date_pay
    paid_for_curs
    paid_for_lesson
    amount
    payment_method
    """
    user = models.ForeignKey(User,
                             on_delete=models.DO_NOTHING,
                            verbose_name="Пользователь",
                            max_length=100)
    date_pay = models.DateField(verbose_name="дата платежа", auto_now=True)
    paid_for_curs = models.ForeignKey(Curs,
                                verbose_name="оплата за курс",
                                 on_delete=models.DO_NOTHING,
                                 **NULLABLE)
    paid_for_lesson = models.ForeignKey(Lesson,
                                verbose_name="оплата за урок",
                                 on_delete=models.DO_NOTHING,
                                 **NULLABLE)
    amount = models.FloatField(verbose_name="суммы оплаты, руб.", default=0.00)
    payment_method = models.CharField(
        verbose_name="Способ оплаты",
        max_length=15,
        choices=[
            ('cash', 'наличные'),
            ('transfer', 'перевод на счет')
        ],
        default='transfer'
    )
    def __str__(self):
        return f'Платеж {self.amount} руб., от {self.date_pay} за {self.paid_for_lesson if self.paid_for_lesson else self.paid_for_curs}, {self.payment_method}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

