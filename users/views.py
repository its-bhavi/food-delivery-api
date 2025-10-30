from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserRegistrationSerializer, UserProfileSerializer


# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)


# Get Current User Profile
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


# Check Username Availability
class CheckUsernameView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({'available': False, 'message': 'Username already taken'})
        return Response({'available': True, 'message': 'Username available'})


# Check Phone Availability
class CheckPhoneView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone = request.data.get('phone')
        if UserProfile.objects.filter(phone=phone).exists():
            return Response({'available': False, 'message': 'Phone number already registered'})
        return Response({'available': True, 'message': 'Phone number available'})
