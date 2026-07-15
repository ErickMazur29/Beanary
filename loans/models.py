from django.db import models
from books.models import Book
from django.conf import settings


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='loans')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loans')
    borrowed_at = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    returned_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Livro emprestado: {self.book.title} - Para: {self.user}"
