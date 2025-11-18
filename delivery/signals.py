from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DeliveryPartner


@receiver(post_save, sender=User)
def create_delivery_partner_profile(sender, instance, created, **kwargs):
    """
    Automatically create DeliveryPartner profile when a user is created with user_type='delivery'
    """
    if created:
        # Check if user has profile with user_type='delivery'
        if hasattr(instance, 'profile'):
            if instance.profile.user_type == 'delivery':
                # Create DeliveryPartner profile
                DeliveryPartner.objects.get_or_create(
                    user=instance,
                    defaults={
                        'phone': instance.profile.phone if hasattr(instance.profile, 'phone') else '',
                        'vehicle_type': 'Bike',  # Default
                        'vehicle_number': 'PENDING',  # Can be updated later
                        'license_number': 'PENDING',  # Can be updated later
                        'status': 'available',
                        'is_verified': False
                    }
                )


@receiver(post_save, sender='users.UserProfile')
def create_delivery_partner_on_profile_update(sender, instance, created, **kwargs):
    """
    Create DeliveryPartner profile when UserProfile is updated to user_type='delivery'
    """
    if instance.user_type == 'delivery':
        # Check if DeliveryPartner profile already exists
        if not hasattr(instance.user, 'delivery_profile'):
            DeliveryPartner.objects.get_or_create(
                user=instance.user,
                defaults={
                    'phone': instance.phone if hasattr(instance, 'phone') else '',
                    'vehicle_type': 'Bike',
                    'vehicle_number': 'PENDING',
                    'license_number': 'PENDING',
                    'status': 'available',
                    'is_verified': False
                }
            )
