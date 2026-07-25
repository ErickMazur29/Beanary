import pandas as pd
from django.core.management.base import BaseCommand
from authors.models import Author


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo CSV com os autores'
        )

    def handle(self, *args, **options):
        file_name = options['file_name']

        df = pd.read_csv(file_name, parse_dates=['birthday'])

        for _, row in df.iterrows():
            if Author.objects.filter(name=row['name'], birthday=row['birthday']).exists():
                self.stdout.write(self.style.WARNING(f"'{row['name']}' já existe, pulando..."))
                continue
            self.stdout.write(self.style.NOTICE(row['name']))

            Author.objects.create(
                name=row['name'],
                birthday=row['birthday'].date(),
                nationality=row['nationality'],
                age=row['age']
            )

        self.stdout.write(self.style.SUCCESS('AUTORES IMPORTADOS COM SUCESSO!!!'))