from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission
from reviews.models import Review
from reviews.serializers import ReviewSerializer, ReviewListSerializer


class ReviewList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewListSerializer
        return ReviewSerializer


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewListSerializer
        return ReviewSerializer
