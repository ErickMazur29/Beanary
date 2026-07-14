from django.db import models
from authors.models import Author
from genres.models import Genre


class Book(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ManyToManyField(Genre, related_name='books')
    author = models.ManyToManyField(Author, related_name='books')
    release_date = models.DateField(null=True, blank=True)
    total_copies = models.PositiveIntegerField(null=True, blank=True)
    resume = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
