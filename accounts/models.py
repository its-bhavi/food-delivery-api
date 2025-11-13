from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    """Extended user account for additional account information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    profile_image = models.ImageField(upload_to='accounts/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Account"

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
