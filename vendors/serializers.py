from rest_framework import serializers
from .models import Restaurant, MenuCategory, MenuItem


# MenuItem Serializer
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image',
            'is_veg',
            'is_available',
            'preparation_time',
            'category',
        ]


# Menu Category Serializer (with items)
class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True, source='menuitem_set')
    
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'description', 'items']


# Restaurant List Serializer (basic info)
class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'image',
            'rating',
            'opening_time',
            'closing_time',
            'is_active',
        ]


# Restaurant Detail Serializer (complete info with menu)
class RestaurantDetailSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    categories = MenuCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'phone',
            'email',
            'address',
            'latitude',
            'longitude',
            'image',
            'rating',
            'opening_time',
            'closing_time',
            'is_active',
            'menu_items',
            'categories',
        ]
