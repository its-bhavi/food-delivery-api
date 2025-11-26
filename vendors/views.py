from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Restaurant, MenuItem, MenuCategory
from .serializers import (
    RestaurantListSerializer,
    RestaurantDetailSerializer,
    MenuItemSerializer,
    MenuCategorySerializer
)


# Restaurant List API (All Restaurants)
class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address']
    ordering_fields = ['rating', 'name']


# Restaurant Detail API (Single Restaurant with Menu)
class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.filter(is_active=True)
    serializer_class = RestaurantDetailSerializer


# Menu Items by Restaurant
class RestaurantMenuView(APIView):
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id, is_active=True)
            menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)
            serializer = MenuItemSerializer(menu_items, many=True)
            return Response({
                'restaurant': restaurant.name,
                'menu_items': serializer.data
            })
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=404)


# Search Restaurants by Location/Name
class RestaurantSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        restaurants = Restaurant.objects.filter(
            name__icontains=query,
            is_active=True
        ) | Restaurant.objects.filter(
            address__icontains=query,
            is_active=True
        )
        serializer = RestaurantListSerializer(restaurants, many=True)
        return Response(serializer.data)


# ========================================
# VENDOR PROFILE MANAGEMENT APIs
# ========================================

@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def vendor_profile_management(request):
    """Manage vendor's restaurant profile (create/update/view)"""
    user = request.user
    
    # Check if user is vendor
    if not hasattr(user, 'profile') or user.profile.user_type != 'vendor':
        return Response({'error': 'Access denied. Not a vendor.'}, status=403)
    
    # GET: Get vendor's restaurant profile
    if request.method == 'GET':
        try:
            restaurant = Restaurant.objects.get(owner=user)
            serializer = RestaurantDetailSerializer(restaurant)
            return Response(serializer.data)
        except Restaurant.DoesNotExist:
            return Response({
                'exists': False,
                'message': 'Please complete your restaurant profile'
            }, status=404)
    
    # POST: Create restaurant profile
    elif request.method == 'POST':
        # Check if restaurant already exists
        if Restaurant.objects.filter(owner=user).exists():
            return Response({'error': 'Restaurant profile already exists. Use PUT to update.'}, status=400)
        
        data = request.data.copy()
        data['owner'] = user.id
        
        # Create restaurant
        restaurant = Restaurant.objects.create(
            owner=user,
            name=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email', user.email),
            address=data.get('address'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            opening_time=data.get('opening_time', '09:00'),
            closing_time=data.get('closing_time', '22:00'),
        )
        
        # Handle image upload if present
        if 'image' in request.FILES:
            restaurant.image = request.FILES['image']
            restaurant.save()
        
        serializer = RestaurantDetailSerializer(restaurant)
        return Response({
            'message': 'Restaurant profile created successfully',
            'restaurant': serializer.data
        }, status=201)
    
    # PUT: Update restaurant profile
    elif request.method == 'PUT':
        try:
            restaurant = Restaurant.objects.get(owner=user)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant profile not found. Use POST to create.'}, status=404)
        
        # Update fields
        data = request.data
        if 'name' in data:
            restaurant.name = data['name']
        if 'phone' in data:
            restaurant.phone = data['phone']
        if 'email' in data:
            restaurant.email = data['email']
        if 'address' in data:
            restaurant.address = data['address']
        if 'latitude' in data:
            restaurant.latitude = data['latitude']
        if 'longitude' in data:
            restaurant.longitude = data['longitude']
        if 'opening_time' in data:
            restaurant.opening_time = data['opening_time']
        if 'closing_time' in data:
            restaurant.closing_time = data['closing_time']
        if 'image' in request.FILES:
            restaurant.image = request.FILES['image']
        
        restaurant.save()
        
        serializer = RestaurantDetailSerializer(restaurant)
        return Response({
            'message': 'Restaurant profile updated successfully',
            'restaurant': serializer.data
        })


# ========================================
# MENU ITEM MANAGEMENT APIs
# ========================================

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def menu_item_management(request, item_id=None):
    """Manage vendor's menu items (create/update/view/delete)"""
    user = request.user
    
    # Check if user is vendor
    if not hasattr(user, 'profile') or user.profile.user_type != 'vendor':
        return Response({'error': 'Access denied. Not a vendor.'}, status=403)
    
    # Get vendor's restaurant
    try:
        restaurant = Restaurant.objects.get(owner=user)
    except Restaurant.DoesNotExist:
        return Response({'error': 'Please create restaurant profile first'}, status=404)
    
    # GET: Get all menu items for vendor's restaurant
    if request.method == 'GET':
        if item_id:
            # Get specific menu item
            try:
                menu_item = MenuItem.objects.get(id=item_id, restaurant=restaurant)
                serializer = MenuItemSerializer(menu_item)
                return Response(serializer.data)
            except MenuItem.DoesNotExist:
                return Response({'error': 'Menu item not found'}, status=404)
        else:
            # Get all menu items
            menu_items = MenuItem.objects.filter(restaurant=restaurant)
            serializer = MenuItemSerializer(menu_items, many=True)
            return Response({
                'count': menu_items.count(),
                'menu_items': serializer.data
            })
    
    # POST: Create new menu item
    elif request.method == 'POST':
        data = request.data.copy()
        
        # Create menu item
        menu_item = MenuItem.objects.create(
            restaurant=restaurant,
            name=data.get('name'),
            description=data.get('description', ''),
            price=data.get('price'),
            category=data.get('category', 'main_course'),
            is_vegetarian=data.get('is_vegetarian', False),
            is_available=data.get('is_available', True),
        )
        
        # Handle image upload
        if 'image' in request.FILES:
            menu_item.image = request.FILES['image']
            menu_item.save()
        
        serializer = MenuItemSerializer(menu_item)
        return Response({
            'message': 'Menu item added successfully',
            'menu_item': serializer.data
        }, status=201)
    
    # PUT: Update menu item
    elif request.method == 'PUT':
        if not item_id:
            return Response({'error': 'Item ID required'}, status=400)
        
        try:
            menu_item = MenuItem.objects.get(id=item_id, restaurant=restaurant)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item not found'}, status=404)
        
        # Update fields
        data = request.data
        if 'name' in data:
            menu_item.name = data['name']
        if 'description' in data:
            menu_item.description = data['description']
        if 'price' in data:
            menu_item.price = data['price']
        if 'category' in data:
            menu_item.category = data['category']
        if 'is_vegetarian' in data:
            menu_item.is_vegetarian = data['is_vegetarian']
        if 'is_available' in data:
            menu_item.is_available = data['is_available']
        if 'image' in request.FILES:
            menu_item.image = request.FILES['image']
        
        menu_item.save()
        
        serializer = MenuItemSerializer(menu_item)
        return Response({
            'message': 'Menu item updated successfully',
            'menu_item': serializer.data
        })
    
    # DELETE: Delete menu item
    elif request.method == 'DELETE':
        if not item_id:
            return Response({'error': 'Item ID required'}, status=400)
        
        try:
            menu_item = MenuItem.objects.get(id=item_id, restaurant=restaurant)
            menu_item.delete()
            return Response({
                'message': 'Menu item deleted successfully'
            }, status=200)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item not found'}, status=404)
