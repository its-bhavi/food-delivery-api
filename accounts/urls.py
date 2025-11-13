from django.urls import path
from .views import (
    UserRegistrationAPIView,
    AccountAPIView,
    UserDetailAPIView
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('profile/', AccountAPIView.as_view(), name='user-account'),
    path('me/', UserDetailAPIView.as_view(), name='user-detail'),
]
