from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from university.models import Lesson, Curs, Subscription
from user_auth.models import User

TEST_USER_EMAIL = 'test@test.ru'
TEST_USER_PASSWORD = '123abc123'


# Create your tests here.
def create_user(*args, **kwargs):
    user = User.objects.create(
        email=TEST_USER_EMAIL,
        first_name='Test',
        last_name='Just User',
        is_staff=False,
        is_superuser=False
    )
    user.set_password(TEST_USER_PASSWORD)
    user.save()
    return user

def create_curs():
    curs1 = Curs.objects.create(
        title="Курс уроков физической культуры",
        preview=None,
        description="Курс для 5-го класса",
        owner=TEST_USER_EMAIL
    )
    curs2 = Curs.objects.create(
        title="Курс уроков математики",
        preview=None,
        description="Курс для 6-го класса",
        owner = TEST_USER_EMAIL
    )

class TestSubscription(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = create_user()
        self.url_token = reverse('token_obtain_pair')
        response = self.client.post(self.url_token,
                                    {"email": TEST_USER_EMAIL,
                                     "password": TEST_USER_PASSWORD
                                     })
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.curs = Curs.objects.create(title='Тестовый курс')
        self.subscription = Subscription.objects.create(user=self.user, curs=self.curs)

    def test_create_subscription(self):
        self.curs2 = Curs.objects.create(title='Еще один тестовый курс')
        url = reverse('subscription_create')
        data = {'curs': self.curs2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.count(), 2)

    def test_retrieve_subscription(self):
        url = reverse('subscription_retrieve', args=[self.subscription.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['curs'], self.curs.id)
        # self.assertEqual(response.data['subscribed'], self.subscription.subscribed)

    def test_update_subscription(self):
        # Создаем новый курс для того, чтобы обновить подписку
        self.curs3 = Curs.objects.create(title='Обновленный тестовый курс')

        url = reverse('subscription_update', args=[self.subscription.id])
        data = {'curs': self.curs3.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_subscription(self):
        url = reverse('subscription_destroy', args=[self.subscription.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)

    def test_list_subscriptions(self):
        url = reverse('subscriptions_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('results')[0]['curs'], self.curs.id)


class TestLessons(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = create_user()
        self.curs = Curs.objects.create(
            title="Тестовый курс",
            preview=None,
            description="Описание тестового курса",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
                        title="Тестовый урок",
                        description="Описание тестового урока",
                        preview="test/url",
                        url_video="https://www.youtube.com/123/",
                        curs=self.curs,
                        owner=self.user
        )

        self.url_token = reverse('token_obtain_pair')
        response = self.client.post(self.url_token,
                                    {"email": TEST_USER_EMAIL,
                                     "password": TEST_USER_PASSWORD
                                     })
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_lesson(self):
        number = Lesson.objects.all().count()
        data =  {
            "title": "Новый тестовый урок",
            "description": "Описание нового тестового урока",
            "url_video": "https://www.youtube.com/123/",
            "curs": self.curs.id
                     }
        response = self.client.post(reverse('lessons_create'),
                                     data
                                     )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), number + 1)

    def test_create_check_owner(self):
        """
        Проверяем, что owner-ом стал пользователь, создавший урок
        """
        data =  {
            "title": "Новый тестовый урок",
            "description": "Описание нового тестового урока",
            "url_video": "https://www.youtube.com/123/",
            "curs": self.curs.id
                     }
        response = self.client.post(reverse('lessons_create'),
                                     data
                                     )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_id = response.data['owner']
        user = User.objects.get(id=user_id)
        self.assertEqual(user, self.user)

    def test_create_bad_url(self):
        data =  {
            "title": "Новый тестовый урок",
            "description": "Описание нового тестового урока",
            "url_video": "https://www.noname.com/123/",
            "curs": self.curs.id
                     }
        response = self.client.post(reverse('lessons_create'),
                                    data
                                    )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "non_field_errors": ["Ссылки на сторонние ресурсы не допускаются! Уроки и курсы должны быть размещены на youtube"]
        })

    def test_update_lesson(self):
        data =  {
            "title": "Обновленный тестовый урок",
            "description": "Описание обновленного тестового урока",
            "url_video": "https://www.youtube.com/125/",
            "curs": self.curs.id
                     }
        response = self.client.put(reverse("lessons_update", args=[self.lesson.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson = Lesson.objects.filter(pk=self.lesson.pk)[0]
        self.assertEqual(lesson.title, "Обновленный тестовый урок")
        self.assertEqual(lesson.description, "Описание обновленного тестового урока")
        self.assertEqual(lesson.url_video, "https://www.youtube.com/125/")

    def test_delete_lesson(self):
        response = self.client.delete(reverse("lessons_destroy", args=[self.lesson.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

class TestCurs(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = create_user()
        self.curs = Curs.objects.create(
            title = "Курс уроков физической культуры",
            amount=5100,
            preview = None,
            description = "Курс для 5-го класса",
            owner=self.user
        )

        self.url_token = reverse('token_obtain_pair')
        response = self.client.post(self.url_token,
                                    {"email": TEST_USER_EMAIL,
                                     "password": TEST_USER_PASSWORD
                                     })
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


    def test_create_check_owner(self):
        """
        Проверяем, что owner-ом стал пользователь, создавший курс
        """
        response = self.client.post(reverse('curs-list'),
                                     {
                                         "title": "Курс уроков физики",
                                         "description": "Курс для 7-го класса"
                                     }
                                     )
        user_id = response.data['owner']
        user = User.objects.get(id=user_id)
        self.assertEqual(user, self.user)

    def test_create(self):
        number_curs = Curs.objects.all().count()
        response = self.client.post(reverse('curs-list'),
                                     {
                                         "title": "Курс уроков биологии",
                                         "description": "Курс для 9-го класса"
                                     }
                                    )
        self.assertEqual(Curs.objects.all().count(), number_curs + 1)

    def test_update_curs(self):
        data = {
              "title": "Курс уроков биологии",
              "description": "Курс для 6-го класса"
          }
        response = self.client.put(reverse("curs-detail", args=[self.curs.pk]), data)
        curs = Curs.objects.filter(pk=self.curs.pk)[0]
        self.assertEqual(curs.title, "Курс уроков биологии")
        self.assertEqual(curs.description, "Курс для 6-го класса")

    def test_send_email_on_curs_update(self):
        mail.outbox = []  # Очищаем список перед тестом
        sub = Subscription.objects.create(curs=self.curs, user=self.user)
        data = {'title': 'Обновленный курс для уведомления'}
        response = self.client.put(reverse('curs-detail', args=[self.curs.pk]), data)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что уведомления отправлены
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Обновление курса')
        self.assertEqual(mail.outbox[0].to, [TEST_USER_EMAIL])


    def test_get_curs_list_status(self):
        self.response = self.client.get(reverse('curs-list'))
        results = self.response.json().get("results")
        expected_results = [
            {
                "title": "Курс уроков физической культуры",
                "preview": None,
                'amount': 5100,
                "description": "Курс для 5-го класса",
                "lessons_count": 0,
                "owner": self.user.id,
                'is_subscribed': False,
                "lessons": [],
            }
        ]
        self.assertEqual(results, expected_results)

    def test_delete_curs(self):
        response = self.client.delete(reverse("curs-detail", args=[self.curs.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Curs.objects.count(), 0)

    def test_get(self):
        response = self.client.get(reverse("curs-detail", args=[self.curs.pk]))
        expected_data = {
                'title': 'Курс уроков физической культуры',
                'preview': None,
                'amount': 5100,
                'description': 'Курс для 5-го класса',
                'lessons': [],
                'owner': self.user.id,
                'is_subscribed': False,
                'lessons_count': 0,
        }

        self.assertEqual(response.json(), expected_data)


class CursTestCase(APITestCase):
    """
    checking status
    """
    def setUp(self):
        super().setUp()
        self.user = create_user()
        self.url_token = reverse('token_obtain_pair')
        response = self.client.post(self.url_token,
                                   {"email": TEST_USER_EMAIL,
                                    "password": TEST_USER_PASSWORD
         })
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.curs = Curs.objects.create(title="Тестовый курс", description="Описание тестового курса", owner=self.user)

    def test_get_curs_list(self):
        response = self.client.get(reverse("curs-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Curs.objects.count(), 1)

    def test_create_curs(self):
        data = {
            "title": "Тестовый курс",
            "description": "Описание тестового курса"
        }
        response = self.client.post(reverse("curs-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Curs.objects.count(), 2)

    def test_update_curs(self):
        data = {
            "title": "Обновленный курс",
            "description": "Описание обновленного курса"
        }
        response = self.client.put(reverse("curs-detail", args=[self.curs.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_send_mail(self):
        data = {"title": "Обновленный курс", "description": "Описание"}

        response = self.client.put(reverse('curs-detail', args=[self.curs.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_curs(self):
        response = self.client.delete(reverse("curs-detail", args=[self.curs.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get(self):
        response = self.client.get(reverse("curs-detail", args=[self.curs.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


