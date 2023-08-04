from django.core.management import BaseCommand

from user_auth.services.services import check_user_last_login


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_user_last_login(args)