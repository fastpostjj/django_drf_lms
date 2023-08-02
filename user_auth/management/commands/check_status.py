from django.core.management import BaseCommand

from payments.services.payment import check_status


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_status(args)