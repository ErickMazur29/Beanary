from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission
from authors.models import Author
from authors.serializers import AuthorSerializer, AuthorListSerializer, AuthorRetrieveSerializer


class AuthorList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Author.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AuthorListSerializer
        return AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Author.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AuthorRetrieveSerializer
        return AuthorSerializer
