from django.urls import path
from . import views


urlpatterns = [
    path('authors/', views.AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>', views.AuthorDetail.as_view(), name='author-detail'),
]
