from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from vendors.models import Restaurant, MenuItem  # ✅ Fixed: vendors (not restaurants)
from .models import Order, OrderItem
from .serializers import OrderDetailSerializer  # ✅ Fixed: Use OrderDetailSerializer
from delivery.models import OrderTracking


# ========================================
# MY ORDERS API (Customer Orders)
# ========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):
    """Get all orders for logged-in customer"""
    user = request.user
    
    # Get all orders for this customer
    orders = Order.objects.filter(customer=user).select_related(
        'restaurant'
    ).prefetch_related('items__menu_item').order_by('-created_at')
    
    serializer = OrderDetailSerializer(orders, many=True)
    return Response(serializer.data)


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
        
        # ✅ First calculate total from items
        total_amount = 0
        validated_items = []
        
        for item_data in data['items']:
            try:
                menu_item = MenuItem.objects.get(id=item_data['menu_item_id'])
                quantity = int(item_data['quantity'])
                price = float(item_data['price'])
                
                validated_items.append({
                    'menu_item': menu_item,
                    'quantity': quantity,
                    'price': price
                })
                
                total_amount += price * quantity
                
            except MenuItem.DoesNotExist:
                return Response({'error': f'Menu item {item_data["menu_item_id"]} not found'}, status=404)
            except (ValueError, KeyError):
                return Response({'error': 'Invalid item data'}, status=400)
        
        # ✅ Calculate delivery charge and tax
        delivery_charge = 50.00  # Fixed delivery charge
        tax_amount = total_amount * 0.05  # 5% GST
        grand_total = total_amount + delivery_charge + tax_amount
        
        # ✅ Create order with all calculated amounts
        order = Order.objects.create(
            customer=user,
            restaurant=restaurant,
            delivery_address=data['delivery_address'],
            customer_phone=data['customer_phone'],
            payment_method=data['payment_method'],
            instructions=data.get('instructions', ''),
            order_number=data.get('order_number', f'ORD{Order.objects.count() + 1}'),
            payment_id=data.get('payment_id', ''),
            total_amount=total_amount,
            delivery_charge=delivery_charge,
            tax_amount=tax_amount,
            grand_total=grand_total,
            status='pending'
        )
        
        # ✅ Add validated order items
        for item in validated_items:
            OrderItem.objects.create(
                order=order,
                menu_item=item['menu_item'],
                quantity=item['quantity'],
                price=item['price']
            )
        
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


# ========================================
# GET ORDER BY ORDER NUMBER OR ID
# ========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_status_by_number(request):
    """Get order status by order number or order ID (query params)"""
    order_number = request.GET.get('order')  # For order number like ORD123
    order_id = request.GET.get('id')  # For order ID like 29
    
    if not order_number and not order_id:
        return Response({'error': 'Order number or ID is required'}, status=400)
    
    try:
        # Try to get by order_number first, then by ID
        if order_number:
            order = Order.objects.select_related(
                'restaurant', 'customer'
            ).prefetch_related('items__menu_item').get(order_number=order_number)
        else:
            order = Order.objects.select_related(
                'restaurant', 'customer'
            ).prefetch_related('items__menu_item').get(id=order_id)
        
        # Check authorization
        user = request.user
        if order.customer != user:
            # Allow restaurant owner to view too
            if not (hasattr(order.restaurant, 'owner') and order.restaurant.owner == user):
                return Response({'error': 'Unauthorized'}, status=403)
        
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)


# ========================================
# GET ORDER DETAIL BY ID (Path Parameter)
# ========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_detail(request, order_id):
    """Get order details by order ID in URL path"""
    try:
        order = Order.objects.select_related(
            'restaurant', 'customer'
        ).prefetch_related('items__menu_item').get(id=order_id)
        
        # Check authorization - customer can view their order
        user = request.user
        if order.customer != user:
            # Allow restaurant owner to view too
            if not (hasattr(order.restaurant, 'owner') and order.restaurant.owner == user):
                return Response({'error': 'Unauthorized'}, status=403)
        
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)


# ========================================
# GET ORDER TRACKING (Live Location)
# ========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_tracking(request, order_id):
    """Get real-time tracking data for order with map coordinates"""
    try:
        order = Order.objects.select_related(
            'restaurant', 'customer'
        ).prefetch_related('items__menu_item').get(id=order_id)
        
        # Check authorization
        user = request.user
        if order.customer != user:
            if not (hasattr(order.restaurant, 'owner') and order.restaurant.owner == user):
                return Response({'error': 'Unauthorized'}, status=403)
        
        # Get tracking data
        try:
            tracking = OrderTracking.objects.select_related('delivery_partner').get(order=order)
        except OrderTracking.DoesNotExist:
            tracking = None
        
        # Prepare response data
        response_data = {
            'order': {
                'id': order.id,
                'order_number': order.order_number,
                'status': order.status,
                'delivery_address': order.delivery_address,
                'restaurant': {
                    'name': order.restaurant.name,
                    'address': order.restaurant.address if hasattr(order.restaurant, 'address') else '',
                    'phone': order.restaurant.phone if hasattr(order.restaurant, 'phone') else ''
                },
                'delivery_partner': None
            },
            'location': {
                # Default restaurant location (you should store these in Restaurant model)
                'restaurant_lat': 28.7041,  # Delhi coordinates as default
                'restaurant_lng': 77.1025,
                # Customer location (parse from delivery_address or store separately)
                'customer_lat': 28.7041,  # You should geocode the delivery_address
                'customer_lng': 77.1025,
                'delivery_lat': None,
                'delivery_lng': None
            }
        }
        
        # Add delivery partner info if available
        if tracking and tracking.delivery_partner:
            response_data['order']['delivery_partner'] = {
                'first_name': tracking.delivery_partner.user.first_name,
                'last_name': tracking.delivery_partner.user.last_name,
                'phone': tracking.delivery_partner.phone,
                'vehicle_type': tracking.delivery_partner.vehicle_type,
                'vehicle_number': tracking.delivery_partner.vehicle_number
            }
            
            # Update delivery partner current location
            if tracking.current_latitude and tracking.current_longitude:
                response_data['location']['delivery_lat'] = float(tracking.current_latitude)
                response_data['location']['delivery_lng'] = float(tracking.current_longitude)
            elif tracking.delivery_partner.current_latitude and tracking.delivery_partner.current_longitude:
                response_data['location']['delivery_lat'] = float(tracking.delivery_partner.current_latitude)
                response_data['location']['delivery_lng'] = float(tracking.delivery_partner.current_longitude)
        
        return Response(response_data)
        
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)
