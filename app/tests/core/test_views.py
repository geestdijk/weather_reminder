from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from pytest_django.asserts import assertTemplateUsed

from core.utils.email_confirmation import account_activation_token


class TestViews:
    def test_confirm_email_view(self, client, sample_user_fixture):
        user = sample_user_fixture
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        assert not user.is_active
        res = client.get(f"/auth/activate/{uid}/{token}/")
        user.refresh_from_db()
        assert user.is_active
        assert res.status_code == 302
        assert res.url == '/auth/login/'

    def test_confirm_email_view_wrong_token(self, client, sample_user_fixture):
        user = sample_user_fixture
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user) + 'foo'
        res = client.get(f"/auth/activate/{uid}/{token}/")
        assert res.status_code == 200
        assertTemplateUsed(res, "auth/account_activation_invalid.html")

    def test_confirm_email_view_wrong_uid(self, client, sample_user_fixture):
        user = sample_user_fixture
        uid = urlsafe_base64_encode(force_bytes(user.pk)) + "making_wrong_uid"
        token = account_activation_token.make_token(user)
        res = client.get(f"/auth/activate/{uid}/{token}/")
        assert res.status_code == 200
        assertTemplateUsed(res, "auth/account_activation_invalid.html")
