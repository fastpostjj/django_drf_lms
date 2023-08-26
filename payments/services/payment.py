import json

import requests
import stripe
from config.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY
from university.models import Curs, Lesson
from payments.models import Paying
from user_auth.models import User
from config.settings import URL_CREATE_PAIMENT_METHODS, URL_CREATE_INTENT, \
    card_cvc, card_number, card_exp_year, card_exp_month
from rest_framework import status


class StripePay():
    api_key = STRIPE_SECRET_KEY
    headers = {'Authorization': f'Bearer {STRIPE_SECRET_KEY}'}
    _payment_intent_id = None
    _payment_method_id = None
    _status= None
    url_intent = URL_CREATE_INTENT
    url_payment_methods = URL_CREATE_PAIMENT_METHODS

    @property
    def payment_intent_id(self):
        return self._payment_intent_id

    @payment_intent_id.setter
    def payment_intent_id(self, id):
        self._payment_intent_id = id

    @property
    def payment_method_id(self):
        return self._payment_method_id

    @payment_method_id.setter
    def payment_method_id(self, id):
        self._payment_method_id = id
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    def is_only_curs_or_lesson(self):
        if self.curs and self.lesson:
            # Если передан и курс и урок, учитываем только курс
            self.lesson = None
            return self.curs
        if not self.curs and not self.lesson:
            # Вызываем исключение, т. к. нет ни курса ни урока для оплаты
            raise KeyError("Не задан курс или урок для оплаты")

    @classmethod
    def create_intent(cls, amount=1000, currency='usd', description="Платеж за курс", metadata={"paid_for_curs":""}, payment_method_types='card'):
        try:
            stripe.api_key = cls.api_key

            # Создать платежный интент
            payment_intent = stripe.PaymentIntent.create(
                amount=round(amount*100),
                currency=currency,
                description=description,
                metadata=metadata,
                payment_method_types=[payment_method_types],
            )
            cls.payment_intent_id = payment_intent["id"]
            status_ = payment_intent["status"]
            client_secret = payment_intent["client_secret"]

            # print("payment_intent=",payment_intent)
            print("payment_intent_id=", cls.payment_intent_id)
            # print('status=', status_)
            # print('client_secret=', client_secret)
            return payment_intent
        except Exception as error:
            print(error)

    @classmethod
    def create_intent_api(cls, amount=1000, currency='usd', description="Платеж за курс", metadata={"paid_for_curs":""}, payment_method_types='card'):
        data = {
            'amount': round(amount*100),
            'currency': currency,
            'description': description,
            'payment_method_types[]': [payment_method_types],
        }
        # Преобразуем metada
        # 'metadata[curs1]': 'curs1', 'metadata[user]': 'user'
        for i in metadata.items():
            data['metadata[' + str(metadata[i[0]]) + ']'] = i[1]
        try:
            response = requests.post(cls.url_intent, headers=cls.headers, data=data)
            if response.status_code == status.HTTP_200_OK:
                payment_intent = response.json()
                cls.payment_intent_id = payment_intent["id"]

                print('payment_intent["id"]=', payment_intent['id'])
                return payment_intent
            else:
                print('response.status_code=', response.status_code)
                # print(response)
                print(response.json())
        except Exception as error:
            print(error)

    @classmethod
    def retrieve_payment_api(cls, id):
        stripe.api_key = cls.api_key
        url = f'{cls.url_intent}/{id}'
        try:
            response = requests.get(url, headers=cls.headers)
            payment_intent = response.json()
            if response.status_code == "200":
                payment_intent_id = payment_intent['id']

                # print("payment_intent=", payment_intent)
                print("payment_intent['id']=", payment_intent['id'])
                return payment_intent
            else:
                # print(url)
                print(response.status_code)
                print(response.json())

        except Exception as error:
            print(error)

    @classmethod
    def retrieve_payment(cls, id):
        try:
            stripe.api_key = cls.api_key
            payment_intent = stripe.PaymentIntent.retrieve(id)
            # print("payment_intent=",payment_intent)
            payment_intent_id = payment_intent['id']
            cls.status = payment_intent.status

            return cls
        except Exception as error:
            print(error)

    @classmethod
    def create_payment_method_api(cls, token="tok_visa"):
        try:
            url = f'{cls.url_payment_methods}'
            data = {"type": 'card', "card[token]": token}
            response = requests.post(url, headers=cls.headers, data=data)
            if response.status_code == status.HTTP_200_OK:
                payment_method = response.json()
                return payment_method
            else:
                # print(response)
                print(response.json())

        except Exception as error:
            print(error)


    @classmethod
    def create_payment_method(cls, token="tok_visa"):
        try:
            stripe.api_key = cls.api_key
            card = {
                'token': token,
            }

            payment_method = stripe.PaymentMethod.create(
                type="card",
                card=card,
            )
            cls.payment_method_id = payment_method.id
            print("payment_method['id']=",payment_method['id'])
            return cls
        except Exception as error:
            print(error)

    def attach_payment_api(self, payment_methods_id):
        try:
            data = {
                "payment_methods": payment_methods_id
            }
            url = f'{self.url_intent}/{self.payment_intent_id}'
            print(url)
            response = requests.post(url, headers=self.headers, data=data)
            if response.status_code == status.HTTP_200_OK:
                payment = response.json()
                print("payment['payment_methods']=",payment['payment_methods'])
                return payment
            else:
                print(response)
        except Exception as error:
            print(error)

    @classmethod
    def confirm_payment(cls, payment_intent_id, payment_method_id):
        print("Подтверждение платежа intent id = ", payment_intent_id, " payment_method_id=",payment_method_id)
        stripe.api_key = cls.api_key
        result = stripe.PaymentIntent.confirm(
            payment_intent_id,
            payment_method=payment_method_id)
        print("result=",result)

        # Обработка платежа
        if result.status == 'succeeded':
            print('Платеж успешно обработан!')
        else:
            print("intent.status=", result.status)
        return result


class StripePaymentMethod():
    """
    Отдельный класс для создания метода платежа, в настоящий момент не используется в проекте
    """
    api_key = STRIPE_SECRET_KEY
    headers = {'Authorization': f'Bearer {STRIPE_SECRET_KEY}'}

    def __init__(self, card={"type": 'card', "card": {'token': 'tok_visa', }}):
        stripe.api_key = self.api_key
        self.card = card
        self._payment_method_id = ""

    @property
    def payment_method_id(self):
        return self._payment_method_id

    @payment_method_id.setter
    def payment_method_id(self, id):
        self._payment_method_id = id


    def create_payment_method(self, card= {'token': 'tok_visa', }):
        try:
            # card = {
            #     'token': 'tok_visa',
            # }

            payment_method = stripe.PaymentMethod.create(
                type="card",
                card=card,
            )
            payment_method.payment_method_id = payment_method['id']
            print("payment_method['id']=", self.payment_method_id)
            return payment_method
        except Exception as error:
            print(error)


def payment(*args, **options):
    """
    Вспомогательный скрипт для запуска в ручном режиме различных команд сервиса stripe
    """
    curs_id = Curs.objects.filter(pk=1)
    user_id = User.objects.filter(pk=1)

    # создаем объект stripe
    stripe_payment = StripePay()
    print("Создаем намерение")
    payment_intent = None

    payment_intent = stripe_payment.create_intent(amount=3000,currency='rub', description="Test payment", metadata={"curs":"curs1","user":"user"})
    if payment_intent:
        payment_intent_id = payment_intent.get('id')

        print("Создаем платежный метод")
        payment_method = stripe_payment.create_payment_method(token="tok_visa")
        print("payment_method=",payment_method)
        # print(payment_method.__dict__)
        if payment_method:
            # payment_method_id = payment_method.get(['id'])
            payment_method_id = payment_method.payment_method_id


            print("Подтверждаем платеж")
            payment_confirm = stripe_payment.confirm_payment(payment_intent_id, payment_method_id)

            print("Проверка статуса")
            intent = stripe_payment.retrieve_payment(payment_intent_id)
            print(intent.status)
        else:
            print("Платежный метод не создан")
    else:
        print("Платежное намерение не создано")

    # 2-й способ через API
    # print("API")
    # print("Создаем намерение")
    # intent_API = stripe_payment.create_intent_api(amount=5000,currency='rub', description="Test payment", metadata={"curs":"curs1","user":"user"})
    # print("intent_API['id']=",intent_API['id'])
    # print("Создаем платежный метод")
    # payment_method_API = stripe_payment.create_payment_method_api(token="tok_visa")
    # print("payment_method=", payment_method_API['id'])
    # stripe_payment.confirm_payment(intent_API['id'],payment_method_API['id'])
    # stripe_payment.retrieve_payment_api(intent_API['id'])
    # print("status=", intent_API['status'])


def check_status(*args):
    """
    скрипт для проверки и обновления статусов
    всех платежей, которые еще не имеют статус "succeeded"
    """
    payments = Paying.objects.filter(id_intent__isnull=False).exclude(
        status='succeeded'
        )
    stripe_object = StripePay()
    for payment in payments:
        result = stripe_object.retrieve_payment(payment.id_intent)
        print(result.status)
        payment.status = result.status
        payment.save()
