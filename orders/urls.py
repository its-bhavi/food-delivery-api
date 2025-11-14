from django.urls import path
from . import views

urlpatterns = [
    # ... existing URLs ...
    
    # Vendor Dashboard
    path('vendor-orders/', views.vendor_orders, name='vendor-orders'),
    
    # Delivery Partner Dashboard
    path('delivery-orders/', views.delivery_orders, name='delivery-orders'),
    
    # Update Order Status
    path('<int:order_id>/update-status/', views.update_order_status, name='update-order-status'),
    
    # Real-time Status
    path('<int:order_id>/realtime-status/', views.order_realtime_status, name='order-realtime-status'),
]
