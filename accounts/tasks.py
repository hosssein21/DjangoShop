# accounts/tasks.py

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_password_reset_email(subject, plain_message, html_message, from_email, recipient_list):
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
    )
