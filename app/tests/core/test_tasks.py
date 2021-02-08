import pytest

from django.template.loader import render_to_string
from pytest_django.asserts import assertTemplateUsed

from core.tasks import confirmation_email


@pytest.mark.django_db
def test_confirmation_email_task(confirmation_email_data,
                                 celery_session_worker,
                                 mailoutbox):
    confirmation_email.delay(confirmation_email_data).wait(2)
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert mail.subject == "Activate your WeatherApp account"
    assert list(mail.to)[0] == confirmation_email_data['to_email']
    with assertTemplateUsed('auth/account_activation_email.html'):
        render_to_string('auth/account_activation_email.html', confirmation_email_data)
