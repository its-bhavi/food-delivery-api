from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DeliveryPartner, OrderTracking
from .serializers import DeliveryPartnerSerializer, OrderTrackingSerializer


# Track Order Location
class OrderTrackingView(generics.RetrieveAPIView):
    serializer_class = OrderTrackingSerializer
    lookup_field = 'order_id'
    
    def get_queryset(self):
        return OrderTracking.objects.all()
    
    def get_object(self):
        order_id = self.kwargs.get('order_id')
        return OrderTracking.objects.get(order_id=order_id)


# Update Delivery Partner Location (for delivery app)
class UpdateDeliveryLocationView(APIView):
    def post(self, request):
        try:
            partner = DeliveryPartner.objects.get(user=request.user)
            latitude = request.data.get('latitude')
            longitude = request.data.get('longitude')
            
            partner.current_latitude = latitude
            partner.current_longitude = longitude
            partner.save()
            
            # Update order tracking if partner has active delivery
            tracking = OrderTracking.objects.filter(
                delivery_partner=partner,
                delivered_at__isnull=True
            ).first()
            
            if tracking:
                tracking.current_latitude = latitude
                tracking.current_longitude = longitude
                tracking.save()
            
            return Response({'message': 'Location updated successfully'})
        except DeliveryPartner.DoesNotExist:
            return Response({'error': 'Delivery partner not found'}, status=404)


# Available Delivery Partners
class AvailablePartnersView(generics.ListAPIView):
    queryset = DeliveryPartner.objects.filter(status='available')
    serializer_class = DeliveryPartnerSerializer
