from rest_framework import generics, views, response, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg
from app.permissions import GlobalDefaultPermission
from books.models import Book
from books.serializers import BookSerializer, BookListSerializer, BookRetrieveSerializer
from reviews.models import Review


class BookList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializer
        return BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookRetrieveSerializer
        return BookSerializer


class BookStats(views.APIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Book.objects.all()

    def get(self, request):
        total_books = self.queryset.count()
        books_by_genre = self.queryset.values('genre__name').annotate(count=Count('id'))
        total_reviews = Review.objects.count()
        avg_rate = Review.objects.aggregate(avg_rating=Avg('rate'))['avg_rating']

        return response.Response(
            data={
                "Total Books": total_books,
                "Books_by_genre": books_by_genre,
                "Total Reviews": total_reviews,
                "Avarage rate": round(avg_rate, 1) if avg_rate else 0  # list comprehesion para validação de campo
            },
            status=status.HTTP_200_OK
        )
