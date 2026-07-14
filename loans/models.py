from django.db import models
from users.models import Profile
from books.models import Book


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='loans')
    borrowed_at = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    returned_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Livro emprestado: {self.book.title} - Para: {self.user}"
