from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from .models import City, UserForecast
from .serializers import (
    MyTokenObtainPairSerializer,
    UserForecastListSerializer,
    UserForecastSerializer,
    UserSerializer,
)
from .utils.email_confirmation import account_activation_token


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer

    @classmethod
    def as_view(cls, **initkwargs):
        # Force enables CSRF protection.  This is needed for unauthenticated API endpoints
        # because DjangoRestFramework relies on SessionAuthentication for CSRF validation
        view = super().as_view(**initkwargs)
        view.csrf_exempt = False
        return view


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class SignUpView(FormView):
    template_name = "core/signup.html"
    form_class = forms.Form


class LoginView(FormView):
    template_name = "core/login.html"
    form_class = forms.Form


class ConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(reverse("auth:login"))
        else:
            return render(request, "auth/account_activation_invalid.html")


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        data = {
            "accessToken": serializer.validated_data["access"],
            "tokenExpire": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
        }
        response = JsonResponse(data)
        response.set_cookie(
            "refresh-token",
            value=serializer.validated_data["refresh"],
            httponly=True,
            samesite="Lax",
            expires=datetime.utcnow() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
        )

        return response


class MyTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        data = {"refresh": request.COOKIES["refresh-token"]}
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response_data = {
            "accessToken": serializer.validated_data["access"],
            "tokenExpire": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class HomeView(TemplateView):
    template_name = "core/home.html"


class UserForecastListApiView(generics.ListAPIView):
    """User's forecasts view"""
    serializer_class = UserForecastListSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        Returns a list of user's cities with corresponding forecasts
        """
        user = self.request.user
        return UserForecast.objects.filter(user=user)


class UserForecastAPIView(generics.CreateAPIView):
    serializer_class = UserForecastSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def delete(self, request, city_name, format=None):
        """Deletes a current user's forecast by city name"""
        user = self.request.user
        city = City.objects.get(name=city_name)
        try:
            user_forecast = UserForecast.objects.get(user=user, city=city)
        except UserForecast.DoesNotExist:
            raise Http404("No UserForecast matches the given query.")
        user_forecast.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ForecastView(LoginRequiredMixin, ListView):
    model = UserForecast
    template_name = 'core/forecast.html'

    def get_queryset(self):
        user = self.request.user
        user_cities_names = UserForecast.objects.filter(user=user)\
            .prefetch_related("city")\
            .values_list("city__name", flat=True)
        cities_to_choose_from = City.objects.values_list('name', flat=True)\
            .exclude(name__in=user_cities_names)
        return cities_to_choose_from
