from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from user import views


urlpatterns = [
    path(
        "register/",
        views.CreateUserView.as_view(),
        name="user-create"
    ),
    path(
        "me/",
        views.ManageUserView.as_view(),
        name="user-manage"
    ),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path(
        "token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify"
    ),
]


app_name = "user"
