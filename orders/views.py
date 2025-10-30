from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer
)


# Create New Order
class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# User's Order History
class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-created_at')


# Order Detail
class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


# Update Order Status (for restaurant/admin)
class OrderStatusUpdateView(APIView):
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            new_status = request.data.get('status')
            
            if new_status in dict(Order._meta.get_field('status').choices):
                order.status = new_status
                order.save()
                serializer = OrderDetailSerializer(order)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Invalid status'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


# Cancel Order (customer can cancel)
class OrderCancelView(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            
            if order.status in ['pending', 'confirmed']:
                order.status = 'cancelled'
                order.save()
                return Response({'message': 'Order cancelled successfully'})
            else:
                return Response(
                    {'error': 'Cannot cancel order at this stage'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
