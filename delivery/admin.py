from django.contrib import admin
from .models import DeliveryPartner, OrderTracking

@admin.register(DeliveryPartner)
class DeliveryPartnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'vehicle_type', 'status', 'rating', 'total_deliveries']
    list_filter = ['status', 'vehicle_type', 'is_verified']
    search_fields = ['user__username', 'phone', 'vehicle_number']

@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ['order', 'delivery_partner', 'distance_km', 'estimated_time_minutes', 'updated_at']
    search_fields = ['order__order_number']
