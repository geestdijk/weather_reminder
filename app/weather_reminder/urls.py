from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from rest_framework_simplejwt import views as jwt_views

from core import views as core_views

from .views import ping


auth_urlpatterns = (
    [
        path("signup/", core_views.SignUpView.as_view(), name="signup"),
        path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
        re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
                core_views.ConfirmEmail.as_view(), name='activate'),
    ],
    "auth",
)

user_urlpatterns = (
    [
        path("create/", core_views.CreateUserView.as_view(), name="create"),
        path("me/", core_views.ManageUserView.as_view(), name="me"),
    ],
    "user",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping/", ping, name="ping"),
    path("auth/", include(auth_urlpatterns)),
    path("api/user/", include(user_urlpatterns)),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
]
