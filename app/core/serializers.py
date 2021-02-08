from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import City, UserForecast

from .tasks import confirmation_email
from .utils.email_confirmation import account_activation_token


class UserSerializer(serializers.ModelSerializer):
    """Serializers for the user objects"""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)
        request = self.context["request"]
        confirmation_email_data = {
            "name": user.name,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "to_email": user.email,
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


class CitySerializer(serializers.ModelSerializer):
    """Serializer for city objects"""

    class Meta:
        model = City
        fields = ("id", "name", "forecast")
        read_only_fields = ('id',)


class NestedCitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = City
        fields = ('name',)


class NestedUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = get_user_model()
        fields = ('id',)
        read_only_fields = ('id',)


class UserForecastListSerializer(serializers.ModelSerializer):
    """Serializer for user forecasts objects"""
    city = CitySerializer()

    class Meta:
        model = UserForecast
        fields = ('city',)
        depth = 1


class UserForecastSerializer(serializers.ModelSerializer):
    """Serializer for creating and deleting user forecasts objects"""
    city = CitySerializer(many=False, read_only=True)
    user = NestedUserSerializer(many=False, read_only=True)

    class Meta:
        model = UserForecast
        fields = ('user', 'city',)

    def create(self, validated_data):
        city_name = self.context['view'].kwargs.get('city_name')
        city = City.objects.get(name=city_name)
        user = self.context['request'].user
        user_forecast, created = UserForecast.objects.get_or_create(user=user, city=city)

        return user_forecast


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serialzer for access and refresh token"""

    def validate(self, attrs):
        data = super().validate(attrs)
        login(self.context["request"], self.user)

        return data
