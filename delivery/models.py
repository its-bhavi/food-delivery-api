from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

# Delivery Partner Status
PARTNER_STATUS = (
    ('available', 'Available'),
    ('busy', 'Busy'),
    ('offline', 'Offline'),
)


# Delivery Partner Model
class DeliveryPartner(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='delivery_profile')
    phone = models.CharField(max_length=15)
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)  # Bike, Scooter, Bicycle
    license_number = models.CharField(max_length=50)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    status = models.CharField(max_length=20, choices=PARTNER_STATUS, default='offline')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_deliveries = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle_type}"


# Order Tracking Model
class OrderTracking(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tracking')
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Tracking Details
    picked_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Current Location
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    
    # Distance and Time
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    estimated_time_minutes = models.IntegerField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking for Order {self.order.order_number}"
