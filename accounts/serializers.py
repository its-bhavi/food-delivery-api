from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account model"""
    
    class Meta:
        model = Account
        fields = ['phone_number', 'address', 'city', 'state', 'pincode', 'profile_image', 'is_verified', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'is_verified']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with account"""
    account = AccountSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'account']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        # Create user account automatically
        Account.objects.create(user=user)
        return user
