from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # because current_app is really a proxy object that is dynamically mapped
    # to the application instance, passing the proxy object would be the same
    # as using current_app directly in the thread. It is needed to access the
    # real application instance stored inside the proxy object ->
    # current_app._get_current_object()
    Thread(
        target=send_async_email, args=(current_app._get_current_object(), msg)
    ).start()
