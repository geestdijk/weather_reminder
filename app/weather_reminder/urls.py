from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path

from core import views as core_views
from setups import views as setups_views

from .views import HelloApiView, HelloTemplateView, ping

auth_urlpatterns = (
    [
        path("signup/", core_views.SignUpView.as_view(), name="signup"),
        path("login/", core_views.LoginView.as_view(), name="login"),
        path("logout/", auth_views.LogoutView.as_view(), name="logout"),
        re_path(
            r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$",
            core_views.ConfirmEmailView.as_view(),
            name="activate",
        ),
    ],
    "auth",
)


user_urlpatterns = (
    [
        path("create/", core_views.CreateUserView.as_view(), name="create"),
        path("me/", core_views.ManageUserView.as_view(), name="me"),
        path("forecast/", core_views.UserForecastListApiView.as_view(), name="my_forecast_api"),
        re_path(r"^forecast/(?P<city_name>[\w\s]+)/$",
                core_views.UserForecastAPIView.as_view(), name="user_forecast_api"),
    ],
    "user",
)

setups_urlpatterns = (
    [
        re_path(r"^(?P<hour>[0-9]{1,2})/$", setups_views.SetupApiView.as_view(), name="create"),
        path("exists/", setups_views.SubscriptionExistsApiView.as_view(), name="setup_exists")
    ],
    "setups",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping/", ping, name="ping"),
    path("api/hello/", HelloApiView.as_view(), name="api-hello"),
    path("hello/", HelloTemplateView.as_view(), name="hello"),
    path("", core_views.HomeView.as_view(), name="home"),
    path("forecast/", core_views.ForecastView.as_view(), name="forecast"),
    path("auth/", include(auth_urlpatterns)),
    path("api/user/", include(user_urlpatterns)),
    path("api/setups/", include(setups_urlpatterns)),
    path(
        "api/token/",
        core_views.MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        core_views.MyTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
