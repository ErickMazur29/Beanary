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

    # Property é usado para transformar este método num atributo do model (um campo)
    # Aqui é o calculo para as copias disponiveis, sendo as copias totais - as que foram emprestadas
    @property
    def copies_available(self):
        return self.total_copies - self.loans.filter(returned_at__isnull=True).count()

    def __str__(self):
        return self.title
