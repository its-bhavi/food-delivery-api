from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Account
from .serializers import (
    UserSerializer, 
    AccountSerializer, 
    UserRegistrationSerializer
)


class UserRegistrationAPIView(generics.CreateAPIView):
    """
    User Registration API
    POST /api/accounts/register/
    Body: {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "password123",
        "password2": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class AccountAPIView(APIView):
    """
    Get or Update User Account
    GET /api/accounts/profile/
    PUT /api/accounts/profile/
    Body: {
        "phone_number": "1234567890",
        "address": "123 Main St",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001"
    }
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)
    
    def put(self, request):
        account, created = Account.objects.get_or_create(user=request.user)
        serializer = AccountSerializer(account, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    Get or Update User Details
    GET /api/accounts/me/
    PUT /api/accounts/me/
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
