from django.contrib.auth import get_user_model
import pytest

from core import models


pytestmark = pytest.mark.django_db


class TestModels:
    def test_user_created_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = "test_password"
        user = get_user_model().objects.create_user(email=email, password=password)

        assert user.email == email
        assert user.check_password(password)

    def test_new_user_email_normalize(self):
        """Test the email for a new user is normalized """
        email = "test@ExAmple.Com"
        user = get_user_model().objects.create_user(email=email)

        assert user.email == email.lower()

    def test_new_user_invalid_email(self):
        """Test creating a new user with no email raises error"""
        with pytest.raises(ValueError) as an_error:
            get_user_model().objects.create_user(email=None, password="Test_pass")
        assert "User must have an email address" == str(an_error.value)

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        email = "test@example.com"
        password = "test_password"
        user = get_user_model().objects.create_superuser(email=email, password=password)

        assert user.is_staff
        assert user.is_superuser

    def test_city_str(self):
        """Test the city string representation"""
        city = models.City.objects.create(name="Port Fourchon")

        assert str(city) == city.name

    def test_user_forecast_str(self, active_user_fixture, sample_city_fixture):
        """Test the UserForecast object string representation"""
        user_city_forecast = models.UserForecast.objects.create(
            city=sample_city_fixture, user=active_user_fixture
        )

        assert (
            str(user_city_forecast)
            == f"City: {sample_city_fixture.name}, User:{active_user_fixture.id}"
        )
