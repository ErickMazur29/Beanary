from rest_framework import serializers
from loans.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

    def validate(self, data):
        book = data['book']
        user = data['user']

        # valida se existem copias disponiveis.
        if book.copies_available <= 0:
            raise serializers.ValidationError("Nenhuma cópia disponivel para este livro.")

        # conta a partir dos retornos, se estiver vazio, é porque nao houve retorno.
        active_loans = Loan.objects.filter(user=user, returned_at__isnull=True).count()
        if active_loans >= user.max_loan_allowed:
            raise serializers.ValidationError("Limite de empréstimos atingido.")

        return data
