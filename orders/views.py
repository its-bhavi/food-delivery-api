from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from vendors.models import Restaurant  # ✅ Fixed: vendors (not restaurants)
from .models import Order
from .serializers import OrderDetailSerializer  # ✅ Fixed: Use OrderDetailSerializer

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
