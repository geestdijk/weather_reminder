from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

from core import models


@pytest.fixture
def client(db):
    """Create a fixture for rest_framework APIClient"""
    client = APIClient()
    return client


@pytest.fixture
def sample_user_fixture(db):
    """Sample user fixture, not active"""
    sample_user = get_user_model().objects.create_user(
        email="test_email@example.com", password="test_password"
    )
    return sample_user


@pytest.fixture
def active_user_fixture(db):
    """Sample active user fixture"""
    active_user = get_user_model().objects.create_user(
        email="active_user_email@example.com",
        password="active_user_password",
        name="Test name",
    )
    active_user.is_active = True
    active_user.save()
    return active_user


@pytest.fixture
def sample_city_fixture(db):
    """Create a sample city"""
    city = models.City.objects.create(name="Sample city")

    return city
