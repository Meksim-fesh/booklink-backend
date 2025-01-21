from django.contrib import admin

from book.models import Author, Book, Chapter, Commentary, Genre


admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Commentary)
