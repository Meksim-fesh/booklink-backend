from django.contrib import admin

from book.models import (
    Author,
    Book,
    BookLike,
    BookView,
    Chapter,
    Commentary,
    Genre
)


admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Commentary)
admin.site.register(BookView)
admin.site.register(BookLike)
