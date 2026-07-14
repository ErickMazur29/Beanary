from django.urls import path
from . import views


urlpatterns = [
    path('loans/', views.LoanList.as_view(), name='loan-list'),
    path('loans/<int:pk>', views.LoanDetail.as_view(), name='loan-detail'),
]
