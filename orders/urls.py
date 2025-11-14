from django.urls import path
from . import views

urlpatterns = [
    # Order Create API
    path('create/', views.create_order, name='create-order'),
    
    # Dashboard APIs
    path('vendor-orders/', views.vendor_orders, name='vendor-orders'),
    path('delivery-orders/', views.delivery_orders, name='delivery-orders'),
    path('<int:order_id>/update-status/', views.update_order_status, name='update-order-status'),
    path('<int:order_id>/realtime-status/', views.order_realtime_status, name='order-realtime-status'),
]
