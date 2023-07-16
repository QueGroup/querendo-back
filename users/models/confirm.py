import binascii
import os
import random
from typing import Any

from django.db import models

from common.models.mixins import TimeBasedMixin
from users.models import User


class EmailConfirmToken(TimeBasedMixin):
    user = models.ForeignKey(
        User,
        related_name="email_confirm_tokens",
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    key = models.CharField(
        verbose_name="Token",
        max_length=64,
        db_index=True,
        unique=True
    )

    class Meta:
        verbose_name = "Email токен"
        verbose_name_plural = "Email токен"

    @staticmethod
    def generate_key():
        length = random.randint(10, 50)
        return binascii.hexlify(os.urandom(50)).decode()[0:length]

    def save(self, *args: Any, **kwargs: Any):
        if not self.key:
            self.key = self.generate_key()
        return super(EmailConfirmToken).save(*args, **kwargs)

    def __str__(self):
        return f"Токен {self.user}"

    # def confirm_email_send(self):
    #     template = Template.objects.filter(
    #         slug='confirm_user_email'
    #     ).first()
    #     url = getattr(settings, 'FRONT_HOST')


#
#     if template:
#         variables = {
#             'full_name': self.user.full_name,
#             'email': self.user.email,
#             'username': self.user.username,
#             'confirm_link': f'{url}/security/email-confirm?token={self.key}'
#         }
#         if getattr(settings, 'USE_CELERY', False):
#             send_email.delay(template_id=template.id, subject=template.theme,
#                              to=[self.user.email], variables=variables)
#
#         else:
#             send_email(template_id=template.id, subject=template.theme,
#                        to=[self.user.email], variables=variables)
#

class ResetPasswordToken(TimeBasedMixin):
    pass
