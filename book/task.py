from book.models import BookMonthView


def clear_month_views():
    BookMonthView.objects.all().delete()
