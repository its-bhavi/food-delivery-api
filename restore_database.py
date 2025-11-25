"""
Database Restore Script for Railway/New Platform
This will import your backed up data to the new database
"""
import os
import django
import json
import glob

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_api.settings')
django.setup()

from django.core import serializers

def restore_database():
    """Import all data from backup JSON files"""
    
    print("🔄 Starting database restore...")
    
    backup_dir = 'database_backup'
    
    if not os.path.exists(backup_dir):
        print(f"❌ Backup directory '{backup_dir}' not found!")
        return
    
    # Find all backup files
    backup_files = sorted(glob.glob(f'{backup_dir}/*.json'))
    
    if not backup_files:
        print("❌ No backup files found!")
        return
    
    print(f"Found {len(backup_files)} backup files\n")
    
    # Restore in order (to handle foreign key dependencies)
    order = ['users', 'restaurants', 'delivery_partners', 'menu_items', 'orders', 'order_items']
    
    for model_name in order:
        matching_files = [f for f in backup_files if model_name in f]
        
        if not matching_files:
            print(f"⚠️ No backup found for {model_name}")
            continue
        
        # Use the latest backup file
        latest_file = matching_files[-1]
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = f.read()
            
            # Deserialize and save objects
            objects = serializers.deserialize('json', data)
            count = 0
            
            for obj in objects:
                obj.save()
                count += 1
            
            print(f"✅ Restored {count} {model_name} from {os.path.basename(latest_file)}")
            
        except Exception as e:
            print(f"❌ Error restoring {model_name}: {e}")
    
    print("\n✅ Database restore completed!")

if __name__ == '__main__':
    confirm = input("⚠️ This will import data. Continue? (yes/no): ")
    if confirm.lower() == 'yes':
        restore_database()
    else:
        print("Restore cancelled.")
