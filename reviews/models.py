from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from books.models import Book
from users.models import Profile


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    rate = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5, 'A avaliação limite é de nota 5!')
        ]
    )
    review = models.TextField(null=True)

    def __str__(self):
        return f"Avaliação de {self.user} - Para o Livro: {self.book.title}"
