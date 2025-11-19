from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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


# ========================================
# DELIVERY PARTNER PROFILE MANAGEMENT API
# ========================================

@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def delivery_partner_profile_management(request):
    """Manage delivery partner profile (create/update/view)"""
    user = request.user
    
    # Check if user is delivery partner
    if not hasattr(user, 'profile') or user.profile.user_type != 'delivery':
        return Response({'error': 'Access denied. Not a delivery partner.'}, status=403)
    
    # GET: Get delivery partner profile
    if request.method == 'GET':
        try:
            partner = DeliveryPartner.objects.get(user=user)
            serializer = DeliveryPartnerSerializer(partner)
            return Response(serializer.data)
        except DeliveryPartner.DoesNotExist:
            return Response({
                'exists': False,
                'message': 'Please complete your delivery partner profile'
            }, status=404)
    
    # POST: Create delivery partner profile
    elif request.method == 'POST':
        # Check if profile already exists
        if DeliveryPartner.objects.filter(user=user).exists():
            return Response({'error': 'Profile already exists. Use PUT to update.'}, status=400)
        
        data = request.data
        
        # Create delivery partner profile
        partner = DeliveryPartner.objects.create(
            user=user,
            phone=data.get('phone'),
            vehicle_type=data.get('vehicle_type', 'Bike'),
            vehicle_number=data.get('vehicle_number'),
            license_number=data.get('license_number', 'PENDING'),
            status='offline'
        )
        
        serializer = DeliveryPartnerSerializer(partner)
        return Response({
            'message': 'Delivery partner profile created successfully',
            'partner': serializer.data
        }, status=201)
    
    # PUT: Update delivery partner profile
    elif request.method == 'PUT':
        try:
            partner = DeliveryPartner.objects.get(user=user)
        except DeliveryPartner.DoesNotExist:
            return Response({'error': 'Profile not found. Use POST to create.'}, status=404)
        
        # Update fields
        data = request.data
        if 'phone' in data:
            partner.phone = data['phone']
        if 'vehicle_type' in data:
            partner.vehicle_type = data['vehicle_type']
        if 'vehicle_number' in data:
            partner.vehicle_number = data['vehicle_number']
        if 'license_number' in data:
            partner.license_number = data['license_number']
        if 'status' in data:
            partner.status = data['status']
        
        partner.save()
        
        serializer = DeliveryPartnerSerializer(partner)
        return Response({
            'message': 'Profile updated successfully',
            'partner': serializer.data
        })
    serializer_class = DeliveryPartnerSerializer
