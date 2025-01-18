from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from book import models, serializers


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class AuthorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class BookViewSet(ModelViewSet):
    queryset = models.Book.objects.prefetch_related("genres", "authors")
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "retrieve":
            return queryset.prefetch_related("chapters")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.BookListSerializer
        if self.action == "retrieve":
            return serializers.BookDetailSerializer
        return serializers.BookSerializer

    @action(
        methods=["post"],
        detail=True,
        url_path="toggle-library",
        url_name="toggle-library",
    )
    def toggle_library(self, request, pk=None):
        book = self.get_object()
        user = self.request.user

        library = user.library.all()

        if book in library:
            user.library.remove(book)
            return Response({"status": "Book was removed"})

        user.library.add(book)
        return Response({"status": "Book was added"})


class ChapterViewSet(
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = models.Chapter.objects.select_related("book")
    serializer_class = serializers.ChapterDetailSerializer
