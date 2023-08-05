from smtplib import SMTPException
from celery import shared_task

from django.core import mail

from config.settings import EMAIL_HOST_USER

@shared_task
def send_email(subject, message_body, email):
    server_answer = ""
    status = 'successfully'
    try:
        with mail.get_connection() as connection:
            email_send = mail.EmailMessage(
                subject,
                message_body,
                EMAIL_HOST_USER,
                [email],
                connection=connection
            )
            email_send.send()

    except SMTPException as error:
        server_answer = error
        status = 'unsuccessfully'
        print('server_answer=', server_answer)
    finally:
        pass
    return status, server_answer