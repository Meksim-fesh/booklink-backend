from django.urls import path, include
from rest_framework.routers import DefaultRouter

from book import views


router = DefaultRouter()

router.register("genres", views.GenreViewSet)
router.register("authors", views.AuthorViewSet)
router.register("books", views.BookViewSet)
router.register("chapters", views.ChapterViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("library/", views.UserLibraryView.as_view(), name="user-library"),
]

app_name = "book"
