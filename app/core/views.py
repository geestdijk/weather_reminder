from django import forms
from django.contrib.auth import get_user_model, login, views as auth_views
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import FormView
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import generics, permissions
from rest_framework_simplejwt import authentication

from .forms import SignUpForm
from .serializers import UserSerializer
from .utils import account_activation_token


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


class ConfirmEmail(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse('admin:login'))
        else:
            return render(request, 'auth/account_activation_invalid.html')
