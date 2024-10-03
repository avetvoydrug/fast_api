import smtplib
from email.message import EmailMessage

from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD

from time import sleep

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379//0', backend='redis://localhost:6379//0')


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'Happy House TODAY'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER
    sleep(15)
    email.set_content(
        '<div>'
        f'<h1 style="color: red;"> Hello, {username}!</h1>'
        'Best wishes, wildlife'
        '</div>',
        subtype='html'
    )
    return email

@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
