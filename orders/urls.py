from django.urls import path
from . import views

urlpatterns = [
    # Customer APIs
    path('my-orders/', views.my_orders, name='my-orders'),
    path('create/', views.create_order, name='create-order'),
    path('status/', views.order_status_by_number, name='order-status-by-number'),  # ?order=ORD123 or ?id=29
    path('<int:order_id>/', views.get_order_detail, name='get-order-detail'),  # Direct order by ID
    path('<int:order_id>/tracking/', views.get_order_tracking, name='get-order-tracking'),  # Live tracking
    
    # Dashboard APIs
    path('vendor-orders/', views.vendor_orders, name='vendor-orders'),
    path('delivery-orders/', views.delivery_orders, name='delivery-orders'),
    path('<int:order_id>/update-status/', views.update_order_status, name='update-order-status'),
    path('<int:order_id>/realtime-status/', views.order_realtime_status, name='order-realtime-status'),
]
