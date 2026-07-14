from django.db import models


class Nationality(models.TextChoices):
    US = "US", "Estados Unidos"
    GB = "GB", "Reino Unido"
    FR = "FR", "França"
    DE = "DE", "Alemanha"
    ES = "ES", "Espanha"
    IT = "IT", "Itália"
    RU = "RU", "Rússia"
    JP = "JP", "Japão"
    IN = "IN", "Índia"
    BR = "BR", "Brasil"


class Author(models.Model):
    name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    nationality = models.CharField(
        max_length=2,
        choices=Nationality.choices,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
