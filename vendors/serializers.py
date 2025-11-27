from rest_framework import serializers
from .models import Restaurant, MenuCategory, MenuItem


# MenuItem Serializer
class MenuItemSerializer(serializers.ModelSerializer):
    # Handle image field properly with full URL
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = [
            'id',
            'name',
            'description',
            'price',
            'image',  # Include original image field
            'image_url',  # Computed full URL
            'is_veg',
            'is_available',
            'preparation_time',
            'category',
        ]
        read_only_fields = ['image_url']
    
    def get_image_url(self, obj):
        """Return full image URL for Railway deployment"""
        if obj.image:
            request = self.context.get('request')
            if request:
                # Build full URL (Railway public URL + media path)
                return request.build_absolute_uri(obj.image.url)
            # Fallback: return relative path
            return obj.image.url
        return None


# Menu Category Serializer (with items)
class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True, source='menuitem_set')
    
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'description', 'items']


# Restaurant List Serializer (basic info)
class RestaurantListSerializer(serializers.ModelSerializer):
    # Properly handle image URL with full path
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'image',  # Include original image field
            'image_url',  # Computed full URL
            'rating',
            'opening_time',
            'closing_time',
            'is_active',
        ]
        read_only_fields = ['image_url']
    
    def get_image_url(self, obj):
        """Return full image URL for Railway deployment"""
        if obj.image:
            request = self.context.get('request')
            if request:
                # Build full URL (Railway public URL + media path)
                return request.build_absolute_uri(obj.image.url)
            # Fallback: return relative path
            return obj.image.url
        return None


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
