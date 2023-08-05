from django.core.management import BaseCommand

from user_auth.models import User


class Command(BaseCommand):
    """
    {
    "email":"admin@admin.pro",
    "password":"123abc123"
}
    {
    "email":"manager@manager.ru",
    "password":"123abc123"
}
    """

    def create_superuser(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.pro',
            first_name='Admin',
            last_name='SuperAdmin',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('123abc123')
        user.save()

    def create_user(self, *args, **options):
        user = User.objects.create(
            email='fastpost@yandex.ru',
            # email='fastpost@rambler.ru',
            first_name='User',
            last_name='Just User',
            is_staff=False,
            is_superuser=False
        )
        user.set_password('123abc123')
        user.save()

    def create_manager(self, *args, **options):
        user = User.objects.create(
            email='manager@manager.ru',
            first_name='manager',
            last_name='moderator',
            is_staff=True,
            is_superuser=False
        )
        user.set_password('123abc123')
        user.save()

    def change_password(self, *args, **options):
        user = User.objects.get(email='fastpost@yandex.ru')
        # user = User.objects.get(email='example@example.com')
        # user = User.objects.get(email='user1@mail.ru')
        # user = User.objects.get(email='fastfastpost@yandex.ru')
        # user = User.objects.get(email='fastfastpost@yandex.ru')
        print(user.check_password('123abc123'))
        user.set_password('123abc123')

        user.save()

    def handle(self, *args, **options):
        # self.create_superuser( *args, **options)
        # self.create_manager( *args, **options)
        self.create_user( *args, **options)
        # self.change_password(*args, **options)