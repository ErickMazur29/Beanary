from django.contrib import admin
from books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date', 'total_copies', 'resume')
    search_fields = ('title',)
