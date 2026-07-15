from rest_framework import serializers
from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    copies_available = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author', 'release_date', 'total_copies', 'copies_available', 'resume']

    def validadte_total_copies(self, value):
        if value > 1000:
            raise serializers.ValidationError("Não é possivel adicionar mais de 1000 cópias de um livro.")
        return value

    def get_copies_available(self, obj):
        return obj.copies_available
