"""
Database Backup Script
This will export all your data before Render expires
"""
import os
import django
import json
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_api.settings')
django.setup()

from django.core import serializers
from django.contrib.auth.models import User
from users.models import UserProfile
from vendors.models import Restaurant, MenuItem
from orders.models import Order, OrderItem
from delivery.models import DeliveryPartner

def backup_database():
    """Export all data to JSON file"""
    
    print("🔄 Starting database backup...")
    
    # Create backup directory
    backup_dir = 'database_backup'
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Backup each model
    models_to_backup = [
        ('auth_users', User),
        ('user_profiles', UserProfile),
        ('restaurants', Restaurant),
        ('menu_items', MenuItem),
        ('orders', Order),
        ('order_items', OrderItem),
        ('delivery_partners', DeliveryPartner),
    ]
    
    for name, model in models_to_backup:
        try:
            data = serializers.serialize('json', model.objects.all(), indent=2)
            filename = f'{backup_dir}/{name}_{timestamp}.json'
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(data)
            
            count = model.objects.count()
            print(f"✅ Backed up {count} {name} to {filename}")
            
        except Exception as e:
            print(f"❌ Error backing up {name}: {e}")
    
    print(f"\n✅ Backup completed! Files saved in '{backup_dir}/' folder")
    print(f"⚠️ IMPORTANT: Keep this folder safe before Render expires!")

if __name__ == '__main__':
    backup_database()
