from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active)

account_activation_token = AccountActivationTokenGenerator()

class SendConfirmationEmail():
    def __init__(self, request, user):
        self.request = request
        self.user = user

    def send_confirmation_email(self):
        current_site = get_current_site(self.request)
        subject = "Activate your WeatherApp account"
        message = render_to_string('auth/account_activation_email.html',{
            'user': self.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': account_activation_token.make_token(self.user),
        })
        email = EmailMessage(subject, message, to=[self.user.email])
        email.send()
