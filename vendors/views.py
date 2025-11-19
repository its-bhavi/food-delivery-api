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
