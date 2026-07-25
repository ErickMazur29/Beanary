import pandas as pd
from django.core.management.base import BaseCommand
from genres.models import Genre


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name',
            type=str,
            help='Nome do arquivo CSV com os gêneros'
        )

    def handle(self, *args, **options):
        file_name = options['file_name']

        df = pd.read_csv(file_name)

        for _, row in df.iterrows():
            if Genre.objects.filter(name=row['name']).exists():
                self.stdout.write(self.style.WARNING(f"'{row['name']}' já existe, pulando..."))
                continue
            self.stdout.write(self.style.NOTICE(row['name']))

            Genre.objects.create(
                name=row['name']
            )

        self.stdout.write(self.style.SUCCESS('GÊNEROS IMPORTADOS COM SUCESSO!!!'))