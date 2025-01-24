from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models.aggregates import Count

from book import models, serializers


class GenreViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class AuthorViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class BookViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = models.Book.objects.prefetch_related("genres", "authors")
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "retrieve":
            return queryset.prefetch_related(
                "chapters",
                "commentaries__replies__author",
                "commentaries__author"
            ).annotate(
                views=Count("viewed_by", distinct=True),
                likes=Count("liked_by", distinct=True),
            )

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

    @action(
            methods=["post"],
            detail=True,
            url_path="toggle-like",
            url_name="toggle-like",
    )
    def toggle_like(self, request, pk=None):
        book = self.get_object()
        user = self.request.user

        like, created = models.BookLike.objects.get_or_create(
            book=book,
            user=user
        )

        if created:
            return Response({"status": "Like was added"})

        like.delete()

        return Response({"status": "Like was removed"})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user

        models.BookView.objects.get_or_create(
            book=instance,
            user=user
        )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserLibraryView(generics.ListAPIView):
    serializer_class = serializers.BookListSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get_queryset(self):
        queryset = models.Book.objects.filter(
            users=self.request.user.id
        ).prefetch_related("genres", "authors")

        return queryset


class ChapterViewSet(
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = models.Chapter.objects.select_related("book")
    serializer_class = serializers.ChapterDetailSerializer


class CommentaryCreateView(generics.GenericAPIView):
    serializer_class = serializers.CommentaryCreateSerializer
    queryset = models.Book.objects.all()

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        user = self.request.user

        serializer = self.serializer_class(
            data=request.data,
            context={
                "request": request,
                "author": user,
                "book": book,
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return HttpResponseRedirect(
            reverse_lazy("book:book-detail", args=[book.id])
        )


class ReplyCreateView(generics.GenericAPIView):
    serializer_class = serializers.ReplyCreateSerializer
    queryset = models.Commentary.objects.all()

    def post(self, request, *args, **kwargs):
        parent = self.get_object()
        user = self.request.user

        serializer = self.serializer_class(
            data=request.data,
            context={
                "request": request,
                "author": user,
                "parent": parent,
            }
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        if parent.parent:
            book_id = parent.parent.book.id
        else:
            book_id = parent.book.id

        return HttpResponseRedirect(
            reverse_lazy("book:book-detail", args=[book_id])
        )
