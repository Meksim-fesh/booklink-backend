from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book import views


router = DefaultRouter()

router.register("genres", views.GenreViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "book"
