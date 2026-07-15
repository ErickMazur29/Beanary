from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    max_loan_allowed = models.PositiveIntegerField(default=3)

    @property
    def can_allow(self):
        return self.max_loan_allowed - self.loans.filter(returned_at__isnull=True).count()

    def __str__(self):
        return f"Perfil de {self.user.username}"
