from django.db import models
from django.contrib.auth.models import User

# User Type Choices
USER_TYPE = (
    ('customer', 'Customer'),
    ('vendor', 'Vendor/Restaurant Owner'),
    ('delivery', 'Delivery Partner'),
)


# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='customer')
    phone = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # Address Details
    default_address = models.TextField(blank=True)
    default_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    default_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Additional Info
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
