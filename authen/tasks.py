from .celery import app
from django.core.mail import send_mail

@app.task
def send_email_async(message_title, message, from_mail, send_to_mail):
    send_mail(message_title, message, from_mail, [send_to_mail])



