from rest_framework import serializers

from book import models


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Genre
        fields = ["id", "name"]


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Author
        fields = ["id", "first_name", "last_name"]


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Chapter
        fields = ["id", "name", "book"]


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Book
        fields = [
            "id",
            "name",
            "genres",
            "authors",
            "pages",
            "summary",
        ]


class BookListSerializer(BookSerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )
    authors = AuthorSerializer(
        many=True,
        read_only=True,
    )


class BookDetailSerializer(BookListSerializer):
    chapters = ChapterSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = models.Book
        fields = [
            "id",
            "name",
            "genres",
            "authors",
            "pages",
            "summary",
            "chapters",
        ]
