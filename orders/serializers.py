from rest_framework import serializers
from .models import Order, OrderItem
from vendors.serializers import MenuItemSerializer


# Order Item Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)
    menu_item_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'menu_item',
            'menu_item_id',
            'quantity',
            'price',
            'subtotal',
            'special_instructions',
        ]
        read_only_fields = ['subtotal']


# Order List Serializer (for listing orders)
class OrderListSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'restaurant_name',
            'status',
            'grand_total',
            'created_at',
        ]


# Order Detail Serializer (complete order info)
class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer_name',
            'restaurant_name',
            'delivery_address',
            'customer_phone',
            'status',
            'total_amount',
            'delivery_charge',
            'tax_amount',
            'grand_total',
            'payment_method',
            'payment_status',
            'instructions',
            'created_at',
            'estimated_delivery_time',
            'items',
        ]


# Order Create Serializer (for placing new orders)
class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'restaurant',
            'delivery_address',
            'delivery_latitude',
            'delivery_longitude',
            'customer_phone',
            'payment_method',
            'instructions',
            'items',
        ]
    
    def create(self, validated_data):
        from decimal import Decimal  # ✅ IMPORT ADD KIYA
        
        items_data = validated_data.pop('items')
        
        # Generate order number
        import random
        order_number = f"ORD{random.randint(100000, 999999)}"
        validated_data['order_number'] = order_number
        
        # Calculate totals (Decimal type use karo, float nahi)
        total = sum(
            Decimal(str(item['price'])) * item['quantity'] 
            for item in items_data
        )
        delivery_charge = Decimal('50.00')  # ✅ Decimal format
        tax = total * Decimal('0.05')  # ✅ Decimal format (5% tax)
        grand_total = total + delivery_charge + tax
        
        validated_data['total_amount'] = total
        validated_data['delivery_charge'] = delivery_charge
        validated_data['tax_amount'] = tax
        validated_data['grand_total'] = grand_total
        
        # Create order
        order = Order.objects.create(**validated_data)
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order


