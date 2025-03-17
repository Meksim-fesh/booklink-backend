import os
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from storages.backends.s3boto3 import S3Boto3Storage
from storages.backends.s3 import S3File


def get_sentinel_user():
    return get_user_model().objects.get_or_create(
        first_name="User", last_name="Deleted", email=None
    )[0]


class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Book(models.Model):
    name = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre, related_name="books")
    authors = models.ManyToManyField(Author, related_name="books")
    pages = models.IntegerField()
    summary = models.TextField()

    def __str__(self):
        return "Book: " + self.name


def get_chapter_s3_path(instance: "Chapter", filename: str) -> os.path:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return f"{instance.book.name}/{filename}"


class ChapterS3Storage(S3Boto3Storage):
    location = "books"


class Chapter(models.Model):
    name = models.CharField(max_length=128)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="chapters"
    )
    serial_number = models.PositiveIntegerField()
    file = models.FileField(
        max_length=256,
        storage=ChapterS3Storage,
        upload_to=get_chapter_s3_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Chapter: " + self.name

    def open(self) -> S3File:
        storage = S3Boto3Storage()
        return storage.open(self.file.name, "rb")


class Commentary(models.Model):
    book = models.ForeignKey(
        Book,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="commentaries"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name="commentaries"
    )
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(book__isnull=False)
                | models.Q(parent__isnull=False),
                name="has_parent_or_book_to_refer_to",
            )
        ]
        verbose_name_plural = "commentaries"

    def __str__(self):
        return str(self.author) + " comment " + self.content


class BookView(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="viewed"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="viewed_by"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("book", "user"),
                name="one_view_for_user_for_book"
            ),
        ]


class BookLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="liked"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="liked_by"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("book", "user"),
                name="one_like_for_user_for_book"
            ),
        ]


class BookMonthView(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="viewed_this_month"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="viewed_by_this_month"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("book", "user"),
                name="one_view_for_user_for_book_this_month"
            ),
        ]
