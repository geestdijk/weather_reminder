# import pytest
# from core.utils.email_confirmation import send_confirmation_email
# from django.template.loader import render_to_string
# from pytest_django.asserts import assertTemplateUsed


# def test_send_confirmation_email(confirmation_email_data, mailoutbox):
#     send_confirmation_email(confirmation_email_data)
#     assert len(mailoutbox) == 1
#     mail = mailoutbox[0]
#     assert mail.subject == "Activate your WeatherApp account"
#     assert list(mail.to)[0] == confirmation_email_data['to_email']
#     with assertTemplateUsed('auth/account_activation_email.html'):
#         render_to_string('auth/account_activation_email.html', confirmation_email_data)
