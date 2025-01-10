from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=64)


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)


class Book(models.Model):
    name = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre, related_name="books")
    authors = models.ManyToManyField(Author, related_name="books")
    pages = models.IntegerField()
    summary = models.TextField()


class Chapter(models.Model):
    name = models.CharField(max_length=128)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
