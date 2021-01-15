from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import mixins, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .tasks import confirmation_email
from .utils import account_activation_token

class UserSerializer(serializers.ModelSerializer):
    """Serializers for the user objects"""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)
        request = self.context['request']
        token = account_activation_token.make_token(user)
        confirmation_email_data = {
            'name': user.name,
            'domain': get_current_site(request).domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'to_email': user.email
        }
        confirmation_email.delay(confirmation_email_data)
        return user

    def update(self, instance, validated_data):
        """Update a user, setting a password correctly, and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        login(self.context['request'], self.user)

        return data
