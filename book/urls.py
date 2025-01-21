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
    path(
        "books/<int:pk>/add-comment/",
        views.CommentaryCreateView.as_view(),
        name="add-comment"
    ),
    path(
        "commentaries/<int:pk>/add-reply/",
        views.ReplyCreateView.as_view(),
        name="add-reply",
    ),
]

app_name = "book"
