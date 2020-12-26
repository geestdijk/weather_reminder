from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

from core import views

from .views import ping

auth_urlpatterns = (
    [
        path("signup/", views.SignUpView.as_view(), name="signup"),
    ],
    "auth",
)

user_urlpatterns = (
    [
        path("create/", views.CreateUserView.as_view(), name="create"),
        path("me/", views.ManageUserView.as_view(), name="me"),
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
