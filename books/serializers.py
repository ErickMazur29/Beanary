from rest_framework import serializers
from django.db.models import Count, Avg
from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    copies_available = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author', 'release_date', 'total_copies', 'copies_available', 'resume']

    def validate_total_copies(self, value):
        if value > 1000:
            raise serializers.ValidationError("Não é possivel adicionar mais de 1000 cópias de um livro.")
        return value

    def get_copies_available(self, obj):
        return obj.copies_available


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author', 'release_date', 'total_copies', 'copies_available', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from authors.serializers import AuthorBookSerializer
        from genres.serializers import GenreSerializer
        self.fields['author'] = AuthorBookSerializer(many=True)
        self.fields['genre'] = GenreSerializer(many=True)


class BookRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    total_rate = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author', 'release_date', 'total_copies', 'copies_available', 'resume', 'total_rate', 'avg_rate', 'comments']

    def get_genre(self, obj):
        return obj.genre.values('name')

    def get_author(self, obj):
        return obj.author.values('name')

    def get_total_rate(self, obj):
        total = obj.reviews.aggregate(Count('rate'))['rate__count']
        if total:
            return total
        return None

    def get_avg_rate(self, obj):
        total = obj.reviews.aggregate(Avg('rate'))['rate__avg']
        if total:
            return round(total, 1)
        return None

    def get_comments(self, obj):
        reviews = obj.reviews.all()
        return [f"Comment: {review.review} - {review.user}" for review in reviews]


# ========= Apenas nested serializers ========= #


# serializer para o Author, apenas.
class BookAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from genres.serializers import GenreSerializer
        self.fields['genre'] = GenreSerializer(many=True)


# serializer para o Genre, apenas.
class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from authors.serializers import AuthorBookSerializer
        self.fields['author'] = AuthorBookSerializer(many=True)
