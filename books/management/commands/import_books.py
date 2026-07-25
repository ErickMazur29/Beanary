import pandas as pd
from django.core.management.base import BaseCommand
from books.models import Book
from authors.models import Author
from genres.models import Genre


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo CSV com os livros'
        )

    def handle(self, *args, **options):
        file_name = options['file_name']

        df = pd.read_csv(file_name, parse_dates=['release_date'])

        for _, row in df.iterrows():
            if Book.objects.filter(title=row['title']).exists():
                self.stdout.write(self.style.WARNING(f"'{row['title']}' já existe, pulando..."))
                continue

            self.stdout.write(self.style.NOTICE(row['title']))

            book = Book.objects.create(
                title=row['title'],
                release_date=row['release_date'].date(),
                total_copies=row['total_copies'],
                resume=row['resume']
            )

            genre_names = [g.strip() for g in row ['genre'].split(';')]
            for genre_name in genre_names:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                book.genre.add(genre)

            author_names = [a.strip() for a in row ['author'].split(';')]
            for author_name in author_names:
                author, _ = Author.objects.get_or_create(name=author_name)
                book.author.add(author)

        self.stdout.write(self.style.SUCCESS('LIVROS IMPORTADOS COM SUCESSO!!!'))