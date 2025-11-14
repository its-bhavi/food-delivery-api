from django.urls import path
from .views import (
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    OrderStatusUpdateView,
    OrderCancelView,
    # Custom Dashboard APIs
    vendor_orders,
    delivery_orders,
    update_order_status,
    order_realtime_status,
)

urlpatterns = [
    # Class-based views
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('my-orders/', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/status/', OrderStatusUpdateView.as_view(), name='order-status'),
    path('<int:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    
    # Custom Dashboard APIs
    path('vendor-orders/', vendor_orders, name='vendor-orders'),
    path('delivery-orders/', delivery_orders, name='delivery-orders'),
    path('<int:order_id>/update-status/', update_order_status, name='update-order-status'),
    path('<int:order_id>/realtime-status/', order_realtime_status, name='order-realtime-status'),
]
