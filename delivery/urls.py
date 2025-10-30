from django.urls import path
from .views import (
    OrderTrackingView,
    UpdateDeliveryLocationView,
    AvailablePartnersView
)

urlpatterns = [
    path('track/<int:order_id>/', OrderTrackingView.as_view(), name='order-tracking'),
    path('update-location/', UpdateDeliveryLocationView.as_view(), name='update-location'),
    path('available/', AvailablePartnersView.as_view(), name='available-partners'),
]
