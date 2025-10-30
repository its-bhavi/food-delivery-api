from rest_framework import serializers
from .models import DeliveryPartner, OrderTracking


# Delivery Partner Serializer
class DeliveryPartnerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = DeliveryPartner
        fields = [
            'id',
            'username',
            'phone',
            'vehicle_type',
            'vehicle_number',
            'current_latitude',
            'current_longitude',
            'status',
            'rating',
            'total_deliveries',
        ]


# Order Tracking Serializer
class OrderTrackingSerializer(serializers.ModelSerializer):
    delivery_partner = DeliveryPartnerSerializer(read_only=True)
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    
    class Meta:
        model = OrderTracking
        fields = [
            'id',
            'order',
            'order_number',
            'delivery_partner',
            'current_latitude',
            'current_longitude',
            'distance_km',
            'estimated_time_minutes',
            'picked_at',
            'delivered_at',
            'updated_at',
        ]
