#!/usr/bin/env python
"""
Railway Database Connection Checker
Ensures DATABASE_URL is properly set before running migrations
"""
import os
import sys

def check_database_connection():
    """Verify DATABASE_URL is configured"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("🚨 CRITICAL ERROR: DATABASE_URL not found!")
        print("   Railway PostgreSQL not connected!")
        print("   Data will be lost on redeploy if using SQLite!")
        print("")
        print("   Fix: Go to Railway Dashboard")
        print("   → Click PostgreSQL service")
        print("   → Click 'Variables' tab")
        print("   → Copy DATABASE_URL")
        print("   → Go to food-delivery-api service")
        print("   → Click 'Variables' tab")
        print("   → Add DATABASE_URL variable")
        sys.exit(1)
    
    # Check if it's PostgreSQL
    if 'postgresql' not in database_url and 'postgres' not in database_url:
        print("⚠️  WARNING: DATABASE_URL doesn't look like PostgreSQL!")
        print(f"   URL starts with: {database_url[:20]}...")
        sys.exit(1)
    
    print("✅ DATABASE_URL is configured")
    print(f"   Database type: PostgreSQL")
    print(f"   URL length: {len(database_url)} characters")
    print("   Data will persist across deployments!")
    return True

if __name__ == '__main__':
    check_database_connection()
