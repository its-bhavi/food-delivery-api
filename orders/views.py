from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from vendors.models import Restaurant, MenuItem  # ✅ Fixed: vendors (not restaurants)
from .models import Order, OrderItem
from .serializers import OrderDetailSerializer  # ✅ Fixed: Use OrderDetailSerializer


# ========================================
# CREATE ORDER API
# ========================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """Create a new order"""
    try:
        user = request.user
        data = request.data
        
        # Validate required fields
        required_fields = ['restaurant', 'delivery_address', 'customer_phone', 'payment_method', 'items']
        for field in required_fields:
            if field not in data:
                return Response({'error': f'{field} is required'}, status=400)
        
        # Get restaurant
        try:
            restaurant = Restaurant.objects.get(id=data['restaurant'])
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=404)
        
        # Create order
        order = Order.objects.create(
            customer=user,
            restaurant=restaurant,
            delivery_address=data['delivery_address'],
            customer_phone=data['customer_phone'],
            payment_method=data['payment_method'],
            instructions=data.get('instructions', ''),
            order_number=data.get('order_number', f'ORD{Order.objects.count() + 1}'),
            payment_id=data.get('payment_id', ''),
            status='pending'
        )
        
        # Add order items
        total_amount = 0
        for item_data in data['items']:
            try:
                menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
                quantity = int(item_data['quantity'])
                price = float(item_data['price'])
                
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=price
                )
                
                total_amount += price * quantity
                
            except MenuItem.DoesNotExist:
                order.delete()
                return Response({'error': f'Menu item {item_data["menu_item_id"]} not found'}, status=404)
            except (ValueError, KeyError):
                order.delete()
                return Response({'error': 'Invalid item data'}, status=400)
        
        # Update order total
        order.total_amount = total_amount
        order.save()
        
        # Return order details
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=201)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)


# ========================================
# VENDOR DASHBOARD API
# ========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_orders(request):
    """Get all orders for vendor's restaurant"""
    user = request.user
    
    # Check if user is vendor - ✅ Fixed: Check UserProfile
    if not hasattr(user, 'profile') or user.profile.user_type != 'vendor':
        return Response({'error': 'Access denied. Not a vendor.'}, status=403)
    
    # Get vendor's restaurant
    try:
        restaurant = Restaurant.objects.get(owner=user)
    except Restaurant.DoesNotExist:
        return Response({'error': 'No restaurant found for this vendor.'}, status=404)
    
    # Get all orders for this restaurant
    orders = Order.objects.filter(restaurant=restaurant).select_related(
        'customer'
    ).prefetch_related('items__menu_item').order_by('-created_at')
    
    serializer = OrderDetailSerializer(orders, many=True)
    return Response(serializer.data)


# ========================================
# DELIVERY PARTNER DASHBOARD API
# ========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delivery_orders(request):
    """Get available and assigned orders for delivery partner"""
    user = request.user
    
    # Check if user is delivery partner - ✅ Fixed: Check UserProfile
    if not hasattr(user, 'profile') or user.profile.user_type != 'delivery':
        return Response({'error': 'Access denied. Not a delivery partner.'}, status=403)
    
    # Get orders:
    # 1. Ready for pickup (status='ready')
    # 2. Currently delivering (status='picked') - ✅ Fixed status name
    # Note: delivery_partner field will be added to Order model
    orders = Order.objects.filter(
        Q(status='ready') | 
        Q(status='picked')
    ).select_related('restaurant', 'customer').prefetch_related(
        'items__menu_item'
    ).order_by('-created_at')
    
    serializer = OrderDetailSerializer(orders, many=True)
    return Response(serializer.data)


# ========================================
# UPDATE ORDER STATUS API
# ========================================
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    """Update order status (vendor or delivery partner)"""
    user = request.user
    new_status = request.data.get('status')
    
    if not new_status:
        return Response({'error': 'Status is required'}, status=400)
    
    # Validate status - ✅ Fixed: Use correct status names from Order model
    valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'picked', 'delivered', 'cancelled']
    if new_status not in valid_statuses:
        return Response({'error': 'Invalid status'}, status=400)
    
    try:
        order = Order.objects.get(id=order_id)
        
        # Authorization check - ✅ Fixed: Check UserProfile
        user_type = user.profile.user_type if hasattr(user, 'profile') else None
        
        if user_type == 'vendor':
            # Vendor can only update their own restaurant orders
            if order.restaurant.owner != user:
                return Response({'error': 'Unauthorized'}, status=403)
        elif user_type == 'delivery':
            # Delivery partner can only update assigned orders
            if order.status not in ['ready', 'picked']:
                return Response({'error': 'Cannot modify this order'}, status=403)
        else:
            return Response({'error': 'Access denied'}, status=403)
        
        # Update status
        order.status = new_status
        
        order.save()
        
        serializer = OrderDetailSerializer(order)
        return Response({
            'message': f'Order status updated to {new_status}',
            'order': serializer.data
        })
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)


# ========================================
# GET SINGLE ORDER DETAILS (REAL-TIME)
# ========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_realtime_status(request, order_id):
    """Get real-time order status for tracking"""
    try:
        order = Order.objects.select_related(
            'restaurant', 'customer', 'delivery_partner'
        ).prefetch_related('items__menu_item').get(id=order_id)
        
        # Check authorization - ✅ Fixed: Simplified check
        user = request.user
        if order.customer != user and order.restaurant.owner != user:
            return Response({'error': 'Unauthorized'}, status=403)
        
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
