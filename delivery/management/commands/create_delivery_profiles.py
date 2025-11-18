from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from delivery.models import DeliveryPartner


class Command(BaseCommand):
    help = 'Create DeliveryPartner profiles for existing delivery users'

    def handle(self, *args, **options):
        # Find all users with user_type='delivery' who don't have DeliveryPartner profile
        delivery_users = User.objects.filter(profile__user_type='delivery')
        
        created_count = 0
        skipped_count = 0
        
        for user in delivery_users:
            # Check if DeliveryPartner profile already exists
            if hasattr(user, 'delivery_profile'):
                self.stdout.write(
                    self.style.WARNING(f'⚠️  DeliveryPartner profile already exists for: {user.username}')
                )
                skipped_count += 1
                continue
            
            # Create DeliveryPartner profile
            delivery_partner = DeliveryPartner.objects.create(
                user=user,
                phone=user.profile.phone if hasattr(user.profile, 'phone') else '',
                vehicle_type='Bike',  # Default
                vehicle_number='PENDING',
                license_number='PENDING',
                status='available',
                is_verified=False
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Created DeliveryPartner profile for: {user.username}')
            )
            created_count += 1
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary:'))
        self.stdout.write(self.style.SUCCESS(f'   ✅ Created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'   ⚠️  Skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'   📝 Total delivery users: {delivery_users.count()}'))
