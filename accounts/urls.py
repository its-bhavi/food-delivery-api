from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileView,
    CheckUsernameView,
    CheckPhoneView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('check-username/', CheckUsernameView.as_view(), name='check-username'),
    path('check-phone/', CheckPhoneView.as_view(), name='check-phone'),
]
