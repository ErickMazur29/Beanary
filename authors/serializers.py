from rest_framework import serializers
from authors.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorListSerializer(serializers.ModelSerializer):
    total_books = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'birthday', 'age', 'nationality', 'total_books']

    def get_total_books(self, obj):
        return obj.books.count()


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    total_books = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'birthday', 'age', 'nationality', 'total_books', 'books']

    def get_total_books(self, obj):
        return obj.books.count()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from books.serializers import BookAuthorSerializer
        self.fields['books'] = BookAuthorSerializer(many=True)


# ========= Apenas nested serializers ========= #


# serializer para Book, apenas.
class AuthorBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
