import time

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()


def send_confirmation_email(data):
    subject = "Activate your WeatherApp account"
    message = render_to_string('auth/account_activation_email.html', data)
    email = EmailMessage(subject, message, to=[data['to_email']])
    return email.send(fail_silently=False)
