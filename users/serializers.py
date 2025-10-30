from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    phone = serializers.CharField(max_length=15)
    user_type = serializers.ChoiceField(choices=['customer', 'vendor', 'delivery'])
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'phone', 'user_type', 'first_name', 'last_name']
    
    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        
        # Check if phone already exists
        if UserProfile.objects.filter(phone=data['phone']).exists():
            raise serializers.ValidationError({"phone": "Phone number already registered"})
        
        return data
    
    def create(self, validated_data):
        # Remove extra fields
        password_confirm = validated_data.pop('password_confirm')
        phone = validated_data.pop('phone')
        user_type = validated_data.pop('user_type')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            phone=phone,
            user_type=user_type
        )
        
        return user


# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'user_type',
            'phone',
            'profile_picture',
            'default_address',
            'default_latitude',
            'default_longitude',
            'date_of_birth',
            'created_at'
        ]
    
    def update(self, instance, validated_data):
        # Update User model fields
        user_data = validated_data.pop('user', {})
        if 'first_name' in user_data:
            instance.user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            instance.user.last_name = user_data['last_name']
        instance.user.save()
        
        # Update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
