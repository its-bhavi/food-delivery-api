from django.urls import path
from .views import (
    RestaurantListView,
    RestaurantDetailView,
    RestaurantMenuView,
    RestaurantSearchView,
    vendor_profile_management
)

urlpatterns = [
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurants/<int:restaurant_id>/menu/', RestaurantMenuView.as_view(), name='restaurant-menu'),
    path('restaurants/search/', RestaurantSearchView.as_view(), name='restaurant-search'),
    
    # Vendor Profile Management
    path('profile/', vendor_profile_management, name='vendor-profile'),
]
