from user_auth.models import User
import datetime


def check_user_last_login(*args, **kwargs):
    daes = 30
    users = User.objects.all()
    now = datetime.datetime.now()
    for user in users:
        if not user.is_staff and not user.is_superuser:
            # админов и менеджеров блокировать не будем
            if not user.last_login:
                # ни разу не заходил
                print("Ни разу не заходил")
                print(user)
                print(user.last_login)
            else:
                print("Подлежат блокировке")
                print(user.last_login)
                print(now - datetime.timedelta(days=days))
                print(now - datetime.timedelta(days=days) > user.last_login)
            # user.is_active
