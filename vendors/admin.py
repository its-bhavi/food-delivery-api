from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'phone', 'rating', 'is_active', 'created_at']
    list_filter = ['is_active', 'rating']
    search_fields = ['name', 'phone', 'email']

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'created_at']
    search_fields = ['name', 'restaurant__name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'price', 'is_veg', 'is_available']
    list_filter = ['is_veg', 'is_available', 'restaurant']
    search_fields = ['name', 'restaurant__name']
