from django.db import models


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


class Chapter(models.Model):
    name = models.CharField(max_length=128)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return "Chapter: " + self.name
