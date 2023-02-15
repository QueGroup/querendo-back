import random

from django.core.mail import send_mail
from django.conf import settings
from .models import QueUser


def send_otp_to_email(email):
    subject = "Your account verification email"
    otp = random.randint(1000, 9999)
    message = f"Your opt is {otp}"
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    user = QueUser.objects.get(email=email)
    user.otp = otp
    user.save()
