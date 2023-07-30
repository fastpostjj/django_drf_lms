import requests
import stripe
from config.settings import STRIPE_SECRET_KEY, STRIPE_PUBLIC_KEY
from university.models import Curs, Lesson
from payments.models import Paying
from user_auth.models import User
from config.settings import URL_CREATE_PAIMENT_METHODS, URL_CREATE_INTENT, card_cvc, card_number, card_exp_year, card_exp_month
from rest_framework import status


def payment(*args, **kwargs):
  # stripe.api_key = STRIPE_SECRET_KEY
  # Тестовый вариант для курса с id 1 и юзера с id 1
  curs = Curs.objects.filter(pk=1)[0]
  user = User.objects.filter(pk=1)[0]
  currency='usd'
  payment_intent = create_intent_api(
    user=user,
    paid_for_curs=curs,
    amount=1000,
    payment_method='card',
    currency=currency
  )
  # print('payment_intent=', payment_intent)
  if payment_intent:
    payment_intent_id = payment_intent.get('id')
    client_secret = payment_intent.get('client_secret')
    print('payment_intent_id=', payment_intent_id)

  data = {
      'type':'card',
      'card[token]':'tok_visa',
    }
  payment_method = create_paiment_method_api(
                       data=data
                       )
  # payment_method = create_payment_method()
  print('payment_method["id"]=',payment_method['id'])

  make_payment_api(
    payment_intent_id=payment_intent_id,
    data={
    "payment_method":payment_method['id'],
    "client_secret":client_secret
  })


def make_payment_api(*args, **kwargs):
  try:
    # amount = kwargs.get('amount')
    payment_intent_id = kwargs.get('payment_intent_id')
    data = kwargs.get('data')
    headers = {'Authorization': f'Bearer {STRIPE_SECRET_KEY}'}
    url = f'{URL_CREATE_INTENT}/{payment_intent_id}/'
    print(url)
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == status.HTTP_200_OK:
      payment = response.json()
      return payment
    else:
      print(response)
  except Exception as error:
    print(error)


def create_intent_api(*args, **kwargs):
  user = kwargs.get('user')
  amount = kwargs.get('amount')
  if 'paid_for_lesson' in kwargs:
    paid_for_lesson = kwargs.get('paid_for_lesson')
  else:
    paid_for_lesson= None
  if 'paid_for_curs' in kwargs:
    paid_for_curs = kwargs.get('paid_for_curs')
  else:
    paid_for_curs = None
  currency = kwargs.get('currency')

  headers = {'Authorization': f'Bearer {STRIPE_SECRET_KEY}'}
  data = {
      'amount': amount,
      'currency': currency,
      'description': 'Payment for course',
      'payment_method_types[]': 'card',
      # 'metadata':{'paid_for_curs':paid_for_curs},
      #              'paid_for_lesson':paid_for_lesson
      #              }]
    }
  try:
    response = requests.post(URL_CREATE_INTENT, headers=headers, data=data)
    if response.status_code == status.HTTP_200_OK:
      payment_intent = response.json()
      # print('payment_intent["id"]=', payment_intent['id'])
      # payment =Paying.objects.create(
      #   user=user,
      #   paid_for_curs=paid_for_curs,
      #   paid_for_lesson=paid_for_lesson,
      #   amount=amount,
      #   payment_method=payment_method
      # )
      # print(payment)
      # payment.save()
      return payment_intent
    else:
      print('response.status_code=',response.status_code)
      # print(response)
      # print(response.json())
  except Exception as error:
    print(error)

def create_paiment_method_api(*args, **kwargs):
  try:
    # print('kwargs=', kwargs)
    payment_intent_id = kwargs.get('payment_intent_id')
    data = kwargs.get('data')
    url = f'{URL_CREATE_PAIMENT_METHODS}'
    headers = {'Authorization': f'Bearer {STRIPE_SECRET_KEY}'}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == status.HTTP_200_OK:
      payment_method = response.json()
      return payment_method
    else:
      print(response)

  except Exception as error:
    print(error)



# 2 вариант через библиотеку stripe

def create_payment_(*args, **kwargs):
  try:
    # payment_intent = create_payment()
    # answer = retrieve_payment(payment_intent['id'])
    # print(answer)
    payment_method = stripe.PaymentMethod.create(
      type="card",
      card={
        "number": "4242424242424242",
        "exp_month": 8,
        "exp_year": 2020,
        "cvc": "314",
      },
    )
    print(payment_method)
    return payment_method
  except Exception as error:
    print(error)

def payment__(*args, **kwargs):
  curs_id = Curs.objects.filter(pk=1)
  try:
    sum = 20
    stripe.api_key = STRIPE_SECRET_KEY
    amount=round(sum*100),
    currency='usd'#'RUB' #'usd'
    payment_method_types='card'
    data = {
      'amount': 1000,
      'currency': 'usd',
      'description': 'Payment for course',
      'metadata[curs_id]': curs_id,
      'payment_method_types[]': 'card',
    }

    # Создать платежный интент
    payment_intent = stripe.PaymentIntent.create(
      amount=2000,
      # amount=amount,
      currency=currency,
      payment_method_types=[payment_method_types],
    )

    id = payment_intent["id"]
    print("payment_intent=",payment_intent)
    print("payment_intent=",id)



    # Создать клиента
    # customer = stripe.Customer.create(
    #   name='Имя Клиента',
    #   email='email@example.com',
    # )
    # print('customer=', customer)

     # Загрузить информацию о платеже
    payment_intent = stripe.PaymentIntent.retrieve(id)
    print("payment_intent=",payment_intent)
    # customer = stripe.Customer.retrieve(
    #   "cu_19YMK02eZvKYlo2CYWjsbgL3",
    #   api_key=STRIPE_SECRET_KEY
    # )
    # customer.capture() # Uses the same API Key.
  except Exception as error:
    print(error)

def create_payment_method(*args, **kwargs):
    # url = 'https://api.stripe.com/v1/payment_intents'
    # headers = {'Authorization': f'Bearer {STRIPE_SECRET_KEY}'}
    #
    # data = {
    #   'amount': 1000,
    #   'currency': 'usd',
    #   'description': 'Payment for course',
    #   'payment_method_types[]': 'card',
    # }
    # print('url=',url)
    # print('headers=',headers)
    # print('data=',data)
    stripe.api_key = STRIPE_SECRET_KEY
    payment_method =  stripe.PaymentMethod.create(
        type='card',
        card={
          'token':'tok_visa',
          # 'number': card_number,
          # 'exp_month': card_exp_month,
          # 'exp_year': card_exp_year,
          # 'cvc': card_cvc,
        })
    # print(payment_method)
    return payment_method


def retrieve_payment(payment_intent_id):
  url = f'https://api.stripe.com/v1/payment_intents/{payment_intent_id}'
  headers = {'Authorization': f'Bearer {STRIPE_SECRET_KEY}'}

  response = requests.get(url, headers=headers)
  payment_intent = response.json()

  return payment_intent