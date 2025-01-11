from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book import views


router = DefaultRouter()

router.register("genres", views.GenreViewSet)
router.register("authors", views.AuthorViewSet)
router.register("books", views.BookViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "book"
