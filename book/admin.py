from django.contrib import admin

from book.models import Author, Book, Chapter, Genre


admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Chapter)
