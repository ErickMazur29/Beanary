from rest_framework import serializers
from loans.models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }

    def validate(self, data):
        request = self.context['request']
        is_staff_or_admin = request.user.groups.filter(name='Staff').exists() or request.user.is_superuser

        # se o usuario nao for Staff nem superuser, o "user" do body é ignorado
        # e sempre vira o proprio perfil de quem esta autenticado.
        if not is_staff_or_admin:
            data['user'] = request.user.profile

        elif 'user' not in data:
            raise serializers.ValidationError("Como staff, você precisa informar o campo 'user'.")

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

class LoanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['book', 'user', 'borrowed_at','due_date', 'returned_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from books.serializers import BookSimpleSerializer
        self.fields['book'] = BookSimpleSerializer()
