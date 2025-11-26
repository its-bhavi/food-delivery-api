"""
Create Django admin superuser for Railway
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_api.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    """Create admin superuser if doesn't exist"""
    
    if User.objects.filter(username='admin').exists():
        print("✅ Admin user already exists")
        return
    
    # Create superuser
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@fooddelivery.com',
        password='Admin@123'
    )
    
    print(f"✅ Created admin superuser")
    print(f"   Username: admin")
    print(f"   Password: Admin@123")
    print(f"   Access: https://food-delivery-api-production-1d00.up.railway.app/admin/")

if __name__ == '__main__':
    create_admin()
