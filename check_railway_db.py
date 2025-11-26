"""
Railway Database Health Check & Data Persistence Script
Run this to verify database connection and check if data persists
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_api.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from vendors.models import Restaurant, MenuItem
from orders.models import Order
from delivery.models import DeliveryPartner

def check_database():
    """Check database connection and data"""
    
    print("=" * 60)
    print("🔍 RAILWAY DATABASE HEALTH CHECK")
    print("=" * 60)
    
    # Database info
    from django.conf import settings
    db_config = settings.DATABASES['default']
    
    print(f"\n📊 Database Configuration:")
    print(f"   Engine: {db_config.get('ENGINE')}")
    print(f"   Name: {db_config.get('NAME', 'N/A')}")
    print(f"   Host: {db_config.get('HOST', 'N/A')}")
    print(f"   Port: {db_config.get('PORT', 'N/A')}")
    
    # Check DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        # Hide password
        safe_url = db_url.split('@')[1] if '@' in db_url else db_url
        print(f"   URL: ...@{safe_url}")
    
    print(f"\n📈 Current Data Count:")
    print(f"   👥 Users: {User.objects.count()}")
    print(f"   📋 Profiles: {UserProfile.objects.count()}")
    print(f"   🍽️  Restaurants: {Restaurant.objects.count()}")
    print(f"   🍕 Menu Items: {MenuItem.objects.count()}")
    print(f"   📦 Orders: {Order.objects.count()}")
    print(f"   🚗 Delivery Partners: {DeliveryPartner.objects.count()}")
    
    print(f"\n👤 User List:")
    for user in User.objects.all()[:10]:
        has_profile = hasattr(user, 'profile')
        profile_type = user.profile.user_type if has_profile else 'N/A'
        print(f"   - {user.username} ({user.email}) | Type: {profile_type}")
    
    print(f"\n🍽️  Restaurant List:")
    for restaurant in Restaurant.objects.all()[:5]:
        print(f"   - {restaurant.name} (Owner: {restaurant.owner.username})")
    
    print(f"\n🍕 Menu Items:")
    for item in MenuItem.objects.all()[:5]:
        print(f"   - {item.name} (₹{item.price}) | Restaurant: {item.restaurant.name}")
    
    print("\n" + "=" * 60)
    print("✅ Database check complete!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        check_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
