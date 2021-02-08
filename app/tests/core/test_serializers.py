import pytest

from core.serializers import UserSerializer

pytestmark = pytest.mark.django_db


def test_user_serializer_update(active_user_fixture):
    serializer = UserSerializer(active_user_fixture, {"email": "active_user_email@example.com",
                                                               "password": "new_password",
                                                               "name": "another name"})
    assert serializer.is_valid()
    assert serializer.errors == {}
    serializer.save()
    active_user_fixture.refresh_from_db()
    assert active_user_fixture.name == "another name"
    assert active_user_fixture.check_password("new_password")
