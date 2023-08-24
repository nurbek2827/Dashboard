import random

from django.core.mail import send_mail
from django.conf import settings



def send_otp(email, code):
    subject = "Your account verificated email"
    message = f"Security code is {code}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])