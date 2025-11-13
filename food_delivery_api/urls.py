from payments.views import RazorpayOrderAPIView, RazorpayPaymentVerifyAPIView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (  # ✅ YEH ADD KARO
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Endpoints
    path('api/users/', include('users.urls')),
    path('api/vendors/', include('vendors.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/delivery/', include('delivery.urls')),
    
    # Razorpay Payment Routes
    path('api/payments/razorpay-order/', RazorpayOrderAPIView.as_view(), name='razorpay-order'),
    path('api/payments/razorpay-verify/', RazorpayPaymentVerifyAPIView.as_view(), name='razorpay-verify'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

