import json

from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from .core.conftest import active_user_fixture

HELLO_API_URL = reverse("api-hello")


def test_hello_world():
    assert "hello_world" == "hello_world"
    assert "foo" != "bar"


def test_ping(client):
    url = reverse("ping")
    res = client.get(url)
    content = json.loads(res.content)
    assert res.status_code == 200
    assert content["ping"] == "pong!"


def test_hello_api_user_is_not_authenticated(client):
    res = client.get(HELLO_API_URL)
    assert res.status_code == 401


def test_hello_api_user_is_authenticated(client, active_user_fixture):
    refresh = RefreshToken.for_user(active_user_fixture)
    print(str(refresh.access_token))
    res = client.get(HELLO_API_URL, HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    assert res.status_code == 200
    assert res.data['greetings'] == 'hello!'
