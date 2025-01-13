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


class AuthorListSerializer(AuthorSerializer):

    class Meta:
        model = models.Author
        fields = ["first_name", "last_name"]


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Chapter
        fields = ["id", "name", "book", "serial_number"]


class ChapterListSerializer(ChapterSerializer):

    class Meta:
        model = models.Chapter
        fields = ["name", "serial_number"]


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
    authors = AuthorListSerializer(
        many=True,
        read_only=True,
    )


class BookDetailSerializer(BookListSerializer):
    chapters = ChapterListSerializer(
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
