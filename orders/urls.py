from django.urls import path
from .views import (
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    OrderStatusUpdateView,
    OrderCancelView
)

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('my-orders/', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_id>/status/', OrderStatusUpdateView.as_view(), name='order-status'),
    path('<int:order_id>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
]
