from rest_framework import serializers
from genres.models import Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class GenreRetrieveSerializer(serializers.ModelSerializer):
    books_by_this_genre = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'books_by_this_genre']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from books.serializers import BookGenreSerializer
        self.fields['books_by_this_genre'] = BookGenreSerializer(many=True, source='books')
