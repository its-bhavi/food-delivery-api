#!/usr/bin/env python
"""
Railway Release Script - Runs before deployment
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"❌ ERROR: {description} failed!")
        sys.exit(1)
    
    print(f"✅ {description} completed successfully")
    return True

def main():
    """Main release process"""
    print("\n🚀 Starting Railway Release Process...\n")
    
    # Step 1: Check database connection
    run_command(
        "python check_database.py",
        "Database Connection Check"
    )
    
    # Step 2: Run migrations
    run_command(
        "python manage.py migrate --noinput",
        "Database Migrations"
    )
    
    # Step 3: Create test user (if needed)
    run_command(
        "python create_test_user.py",
        "Create Test User"
    )
    
    # Step 4: Create admin (if needed)
    run_command(
        "python create_admin.py",
        "Create Admin User"
    )
    
    print("\n✅ Release process completed successfully!")
    print("🚀 Starting web server...\n")

if __name__ == '__main__':
    main()
