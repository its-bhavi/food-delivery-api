from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import razorpay
import logging

logger = logging.getLogger(__name__)

class RazorpayOrderAPIView(APIView):
    """
    Create Razorpay order for payment
    POST /api/payments/razorpay-order/
    Body: {
        "amount": 500.50,  # Amount in rupees
        "order_number": "ORD123",  # Your order reference
        "receipt": "receipt_001"  # Optional
    }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Get amount from request (in rupees)
            amount_rupees = float(request.data.get('amount', 0))
            amount_paise = int(amount_rupees * 100)  # Convert to paise
            
            # Receipt ID (optional)
            order_number = request.data.get('order_number', 'ORDER-001')
            receipt_id = f"fd-{request.user.id}-{order_number}"
            
            # Create Razorpay client
            client = razorpay.Client(auth=(
                settings.RAZORPAY_KEY_ID, 
                settings.RAZORPAY_KEY_SECRET
            ))
            
            # Create order
            order_data = {
                'amount': amount_paise,
                'currency': 'INR',
                'receipt': receipt_id,
                'payment_capture': '1'  # Auto capture
            }
            
            razorpay_order = client.order.create(data=order_data)
            
            logger.info(f"Razorpay order created: {razorpay_order['id']}")
            
            # Return order details to frontend
            return Response({
                'success': True,
                'id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
                'currency': razorpay_order['currency'],
                'key_id': settings.RAZORPAY_KEY_ID,
                'order_number': order_number
            }, status=201)
            
        except Exception as e:
            logger.error(f"Razorpay order creation failed: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)


class RazorpayPaymentVerifyAPIView(APIView):
    """
    Verify Razorpay payment signature
    POST /api/payments/razorpay-verify/
    Body: {
        "razorpay_order_id": "order_xxx",
        "razorpay_payment_id": "pay_xxx",
        "razorpay_signature": "signature_xxx"
    }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            razorpay_order_id = request.data.get('razorpay_order_id')
            razorpay_payment_id = request.data.get('razorpay_payment_id')
            razorpay_signature = request.data.get('razorpay_signature')
            
            # Create Razorpay client
            client = razorpay.Client(auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            ))
            
            # Verify signature
            params = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            client.utility.verify_payment_signature(params)
            
            logger.info(f"Payment verified: {razorpay_payment_id}")
            
            return Response({
                'success': True,
                'message': 'Payment verified successfully',
                'payment_id': razorpay_payment_id
            }, status=200)
            
        except razorpay.errors.SignatureVerificationError as e:
            logger.error(f"Payment verification failed: {str(e)}")
            return Response({
                'success': False,
                'error': 'Invalid payment signature'
            }, status=400)
            
        except Exception as e:
            logger.error(f"Payment verification error: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=400)
