import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
ME_URL = reverse("user:me")
TOKEN_PAIR_URL = reverse("token_obtain_pair")
REFRESH_TOKEN_URL = reverse("token_refresh")

pytestmark = pytest.mark.django_db


class TestPublicUserAPI:
    def test_create_valid_user_success(self, client):
        """Test creating user with valid payload is successful"""
        payload = {
            "email": "test1@example.com",
            "password": "test_password",
            "name": "Test name",
        }
        res = client.post(CREATE_USER_URL, payload)

        assert res.status_code == status.HTTP_201_CREATED
        user = get_user_model().objects.get(**res.data)
        assert user.check_password(payload["password"])
        assert "password" not in res.data

    def test_user_exists(self, client, sample_user_fixture):
        """Test creating user that already exists"""
        payload = {"email": "test_email@example.com", "password": "test_password"}
        res = client.post(CREATE_USER_URL, payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_too_short(self, client):
        """Test that the password must be at least 6 characters long"""
        payload = {"email": "test_email@example.com", "password": "passw"}
        res = client.post(CREATE_USER_URL, payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert not get_user_model().objects.filter(email=payload["email"]).exists()

    def test_create_jwt_token_pair_for_user(self, client, active_user_fixture):
        """Test that a JWT token pair is created for user"""

        payload = {
            "email": "active_user_email@example.com",
            "password": "active_user_password",
        }
        res = client.post(TOKEN_PAIR_URL, payload)
        assert res.status_code == status.HTTP_200_OK
        assert "accessToken" in res.json()
        assert "refresh-token" in client.cookies

    def test_create_jwt_token_pair_for_user_wrong_password(self, client, active_user_fixture):
        """Test that wrong password raises Error"""
        payload = {
            "email": "active_user_email@example.com",
            "password": "wrong_password",
        }
        res = client.post(TOKEN_PAIR_URL, payload)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        assert res.data['detail'] == 'No active account found with the given credentials'

    def test_obtain_new_access_token_using_refresh_token(
        self, client, active_user_fixture
    ):
        """Test obtaining new access token using refresh token"""
        payload = {
            "email": "active_user_email@example.com",
            "password": "active_user_password",
        }
        res = client.post(TOKEN_PAIR_URL, payload)
        # refresh_token = client.cookies["refresh-token"].value
        res = client.post(REFRESH_TOKEN_URL, {})
        assert res.status_code == status.HTTP_200_OK
        assert "accessToken" in res.json()

    def test_obtain_new_access_token_using_wrong_refresh_token(
        self, client
    ):
        """Test failure obtaining new access token using wrong refresh token"""
        client.cookies["refresh-token"] = "wrong_refresh_token"
        res = client.post(REFRESH_TOKEN_URL, {})
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        assert res.data['detail'] == 'Token is invalid or expired'


class TestPrivateUserAPI:
    @pytest.fixture(autouse=True)
    def setup_method(self, client, active_user_fixture):
        self.active_user = active_user_fixture
        self.client = client
        self.client.force_authenticate(user=self.active_user)

    def test_retrive_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {
            "email": self.active_user.email,
            "name": self.active_user.name,
        }

    def test_post_me_not_allowed(self):
        """Test that POST method is not allowed on "me" url"""
        res = self.client.post(ME_URL, {})

        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update_user_profile(self):
        """Test updating user profile for an authenticated user"""
        payload = {"name": "new_name", "password": "new_password"}
        self.client.patch(ME_URL, payload)
        self.active_user.refresh_from_db()
        assert self.active_user.name == payload["name"]
        assert self.active_user.check_password(payload["password"])
