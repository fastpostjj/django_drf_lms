from celery import shared_task
from payments.services.payment import check_status


@shared_task
def check_status_payment(*args):
    check_status(args)
