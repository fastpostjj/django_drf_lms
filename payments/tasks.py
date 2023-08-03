from celery import shared_task
from payments.services.payment import check_status
from config.settings import BASE_DIR
import os


@shared_task
def check_status_payment(*args):
    check_status(args)
    file_name = str(BASE_DIR) + os.sep + "log.txt"
    print(file_name)
    with open(file_name, "a") as file:
        file.write("check_status\n")
