from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
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
