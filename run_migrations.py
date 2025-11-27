#!/usr/bin/env python
"""
Railway Migration Script - Run ONLY when needed
DO NOT run on every deployment!
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery_api.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def check_database_connection():
    """Check if database is accessible"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def run_migrations():
    """Run migrations safely"""
    if not check_database_connection():
        print("⚠️ Cannot run migrations - database not accessible!")
        sys.exit(1)
    
    print("\n🔄 Running migrations...")
    try:
        call_command('migrate', '--noinput')
        print("✅ Migrations completed successfully!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    print("=" * 50)
    print("Railway Migration Script")
    print("=" * 50)
    
    # Check if DATABASE_URL exists
    if not os.getenv('DATABASE_URL'):
        print("⚠️ WARNING: DATABASE_URL not found!")
        print("⚠️ Make sure PostgreSQL is connected in Railway!")
        sys.exit(1)
    
    run_migrations()
