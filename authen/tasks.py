from .celery import app

@app.task
def send_email_async(email, message_title, message, send_type="send"):
    send_mail(message_title, message, None, [email])



