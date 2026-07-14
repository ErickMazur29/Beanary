from django.urls import path
from . import views


urlpatterns = [
    path('genres/', views.GenreList.as_view(), name='genre-list'),
    path('genres/<int:pk>', views.GenreDetail.as_view(), name='genre-detail'),
]
