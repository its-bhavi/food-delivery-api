from django.db import models
from django.contrib.auth.models import User
from vendors.models import Restaurant, MenuItem

# Order Status Choices
ORDER_STATUS = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('preparing', 'Preparing'),
    ('ready', 'Ready for Pickup'),
    ('picked', 'Picked by Delivery Partner'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

# Payment Method Choices
PAYMENT_METHOD = (
    ('cod', 'Cash on Delivery'),
    ('online', 'Online Payment'),
    ('upi', 'UPI'),
)


# Order Model
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_orders')
    order_number = models.CharField(max_length=20, unique=True)
    
    # Delivery Details
    delivery_address = models.TextField()
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    customer_phone = models.CharField(max_length=15)
    
    # Order Details
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment Details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Special Instructions
    instructions = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.customer.username}"

    class Meta:
        ordering = ['-created_at']


# Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)

# Signal to create tracking automatically when order is confirmed
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Order)
def create_order_tracking(sender, instance, created, **kwargs):
    from delivery.models import OrderTracking, DeliveryPartner
    
    # Only create tracking when order is confirmed
    if instance.status == 'confirmed' and not hasattr(instance, 'tracking'):
        # Get available delivery partner
        partner = DeliveryPartner.objects.filter(status='available').first()
        
        if partner:
            # Create tracking
            OrderTracking.objects.create(
                order=instance,
                delivery_partner=partner,
                distance_km=5.0,  # Sample distance
                estimated_time_minutes=30
            )
            
            # Update partner status
            partner.status = 'busy'
            partner.save()
