from django.urls import path
from . import views

urlpatterns = [
    # Customer APIs
    path('my-orders/', views.my_orders, name='my-orders'),
    path('create/', views.create_order, name='create-order'),
    path('status/', views.order_status_by_number, name='order-status-by-number'),  # ?order=ORD123 or ?id=29
    
    # Order Status Update (must be BEFORE generic <int:order_id>/)
    path('<int:order_id>/update-status/', views.update_order_status, name='update-order-status'),
    path('<int:order_id>/update-location/', views.update_delivery_location, name='update-delivery-location'),  # Live GPS
    path('<int:order_id>/tracking/', views.get_order_tracking, name='get-order-tracking'),  # Live tracking
    path('<int:order_id>/realtime-status/', views.order_realtime_status, name='order-realtime-status'),
    
    # Generic order detail (must be AFTER specific paths)
    path('<int:order_id>/', views.get_order_detail, name='get-order-detail'),  # Direct order by ID
    
    # Dashboard APIs
    path('vendor-orders/', views.vendor_orders, name='vendor-orders'),
    path('delivery-orders/', views.delivery_orders, name='delivery-orders'),
]
