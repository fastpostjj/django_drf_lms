from django.core.management import BaseCommand

from payments.services.payment import payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment(args)