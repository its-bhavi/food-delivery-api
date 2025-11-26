"""
Quick user creation script for Railway
Run this locally then push to Railway or run via Railway shell
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_api.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile

def create_test_user():
    """Create kapil123 user for testing"""
    
    # Check if user exists
    if User.objects.filter(username='kapil123').exists():
        print("✅ User 'kapil123' already exists")
        return
    
    # Create user
    user = User.objects.create_user(
        username='kapil123',
        email='kapil@example.com',
        password='Kapil123@',  # Same password as before
        first_name='Kapil',
        last_name='Test'
    )
    
    # Create profile
    UserProfile.objects.create(
        user=user,
        phone='9876543210',
        user_type='customer'
    )
    
    print(f"✅ Created user: {user.username}")
    print(f"   Email: {user.email}")
    print(f"   Password: Kapil123@")
    print(f"   Phone: 9876543210")
    print(f"   Type: customer")

if __name__ == '__main__':
    create_test_user()
