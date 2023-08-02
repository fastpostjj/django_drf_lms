from django.db import models

from config.settings import NULLABLE
from university.models import Curs, Lesson
from user_auth.models import User


# Create your models here.


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
    amount = models.FloatField(verbose_name="суммы оплаты, руб.", default=0.00, **NULLABLE)
    payment_method = models.CharField(
        verbose_name="Способ оплаты",
        max_length=15,
        choices=[
            ('cash', 'наличные'),
            ('transfer', 'перевод на счет'),
            ('card','оплата картой')
        ],
        default='transfer'
    )
    id_intent = models.CharField(verbose_name="id намерения платежа", max_length=50, **NULLABLE)
    status = models.CharField(verbose_name="статус платежа", max_length=200, **NULLABLE)

    def __str__(self):
        return f'Платеж {self.amount} руб., от {self.date_pay} за {self.paid_for_lesson if self.paid_for_lesson else self.paid_for_curs}, {self.payment_method}, {self.status}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
