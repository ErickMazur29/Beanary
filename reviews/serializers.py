from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['book', 'user', 'rate', 'review']

    def validate(self, data):
        request = self.context['request']
        is_staff_or_admin = request.user.groups.filter(name='Staff').exists() or request.user.is_superuser

        # se o usuario nao for Staff nem superuser, o "user" do body é ignorado
        # e sempre vira o proprio perfil de quem esta autenticado.
        if not is_staff_or_admin:
            data['user'] = request.user.profile

        elif 'user' not in data:
            raise serializers.ValidationError("Como staff, você precisa informar o campo 'user'.")

        return data

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            from books.serializers import BookSimpleSerializer
            self.fields['book'] = BookSimpleSerializer()
