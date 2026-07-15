from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission
from loans.models import Loan
from loans.serializers import LoanSerializer


class LoanList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
