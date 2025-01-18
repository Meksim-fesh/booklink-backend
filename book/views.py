from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

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


class ChapterViewSet(
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = models.Chapter.objects.select_related("book")
    serializer_class = serializers.ChapterDetailSerializer
