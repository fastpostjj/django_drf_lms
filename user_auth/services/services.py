from user_auth.models import User
import datetime

import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule
def set_schedule(*args, **kwargs):

    schedule, created = IntervalSchedule.objects.get_or_create(
         every=10,
         period=IntervalSchedule.SECONDS,
     )

    PeriodicTask.objects.create(
         interval=schedule,
         name='Importing contacts',
         task='user_auth.tasks.task_check_last_login',
         args=json.dumps(['arg1', 'arg2']),
         kwargs=json.dumps({
            'be_careful': True,
         }),
         expires=datetime.utcnow() + timedelta(seconds=30)
     )


def check_user_last_login(*args, **kwargs):
    days = 30
    users = User.objects.all()
    for user in users:
        if not user.is_staff and not user.is_superuser:
            # админов и менеджеров блокировать не будем
            if not user.last_login:
                # ни разу не заходил
                print("Ни разу не заходил")
                print("user=",user," user.is_active=",user.is_active, " last_login=", user.last_login)
            elif datetime.datetime.now().replace(tzinfo=user.last_login.tzinfo) - datetime.timedelta(days=days) > user.last_login:
                # user_timezone = user.last_login.tzinfo
                # now = datetime.datetime.now()
                # now = now.replace(tzinfo=user_timezone)
                print("Подлежат блокировке")
                print("user=",user," user.is_active=",user.is_active, " last_login=", user.last_login)
                user.is_active = False
                user.save()

            else:
                print(f"Заходили менее {days} дней назад, не надо блокировать:")
                print("user=",user," user.is_active=",user.is_active, " last_login=", user.last_login)
