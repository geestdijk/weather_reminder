import pytest
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from core import models
from core.utils import account_activation_token


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


@pytest.fixture
def confirmation_email_data(active_user_fixture):
    user = active_user_fixture
    request = HttpRequest()
    request.META = {
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "8000",
    }
    confirmation_email_data = {
        "name": user.name,
        "domain": get_current_site(request).domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
        "to_email": user.email,
    }
    return confirmation_email_data
    
