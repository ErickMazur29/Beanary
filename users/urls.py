from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.ProfileList.as_view(), name='user-list'),
    path('users/<int:pk>', views.ProfileDetail.as_view(), name='user-detail'),
]
