from rest_framework import serializers
from .models import Restaurant, MenuCategory, MenuItem


# MenuItem Serializer
class MenuItemSerializer(serializers.ModelSerializer):
    # Handle image field gracefully
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image_url',
            'is_veg',
            'is_available',
            'preparation_time',
            'category',
        ]
    
    def get_image_url(self, obj):
        # Return None for now - can add Cloudinary/S3 later
        return None


# Menu Category Serializer (with items)
class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True, source='menuitem_set')
    
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'description', 'items']


# Restaurant List Serializer (basic info)
class RestaurantListSerializer(serializers.ModelSerializer):
    # Temporarily exclude image to avoid media file errors on Railway
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'image_url',
            'rating',
            'opening_time',
            'closing_time',
            'is_active',
        ]
    
    def get_image_url(self, obj):
        # Return placeholder or None if image doesn't exist
        return None  # Can add real image URL later


# Restaurant Detail Serializer (complete info with menu)
class RestaurantDetailSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True)
    categories = MenuCategorySerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    
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
            'image_url',
            'rating',
            'opening_time',
            'closing_time',
            'is_active',
            'menu_items',
            'categories',
        ]
    
    def get_image_url(self, obj):
        # Return None for now - can add Cloudinary/S3 later
        return None
