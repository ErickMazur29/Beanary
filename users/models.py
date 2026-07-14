from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    max_loan_allowed = models.PositiveBigIntegerField(default=3)

    def __str__(self):
        return f"Perfil de {self.user.username}"
