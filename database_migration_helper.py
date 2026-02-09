#!/usr/bin/env python3
"""
Database Migration Helper Script
This script helps with migrating the database to a new provider
"""

import os
import subprocess
import sys
from pathlib import Path

def check_prerequisites():
    """Check if required tools are installed"""
    print("Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        return False
    
    # Check if pip is available
    try:
        subprocess.run(["pip", "--version"], capture_output=True, check=True)
        print("✅ pip available")
    except subprocess.CalledProcessError:
        print("❌ pip not available")
        return False
    
    return True

def create_requirements_file():
    """Create/update requirements file for deployment"""
    print("Creating production requirements...")
    
    requirements_content = """# Production requirements for ME Newsletter
-r requirements/base.txt
gunicorn==20.1.0
psycopg2-binary==2.9.5
whitenoise==6.2.0
"""
    
    with open("requirements/production.txt", "w") as f:
        f.write(requirements_content)
    
    print("✅ Production requirements created")

def setup_supabase_migration():
    """Instructions for Supabase migration"""
    print("\n" + "="*50)
    print("SUPABASE DATABASE SETUP INSTRUCTIONS")
    print("="*50)
    print("1. Go to https://supabase.com")
    print("2. Sign up for free account")
    print("3. Create new project")
    print("4. Note your database credentials:")
    print("   - Database URL")
    print("   - Username")
    print("   - Password")
    print("5. Run this command to test connection:")
    print("   psql 'postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]'")
    print("="*50)

def setup_render_deployment():
    """Instructions for Render deployment"""
    print("\n" + "="*50)
    print("RENDER DEPLOYMENT INSTRUCTIONS")
    print("="*50)
    print("1. Go to https://render.com")
    print("2. Sign up for free account")
    print("3. Click 'New Web Service'")
    print("4. Connect your GitHub repository")
    print("5. Configure settings:")
    print("   - Name: me-newsletter-backend")
    print("   - Runtime: Python 3")
    print("   - Build Command: pip install -r requirements/production.txt")
    print("   - Start Command: gunicorn config.wsgi:application")
    print("6. Add environment variables:")
    print("   - DATABASE_URL (from Supabase)")
    print("   - DJANGO_SECRET_KEY (generate strong key)")
    print("   - DJANGO_DEBUG=False")
    print("   - DJANGO_ALLOWED_HOSTS=your-app.onrender.com")
    print("="*50)

def generate_secret_key():
    """Generate Django secret key"""
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))
    return secret_key

def main():
    print("ME Newsletter Database Migration Helper")
    print("="*40)
    
    if not check_prerequisites():
        print("Please install required prerequisites and try again.")
        return
    
    create_requirements_file()
    
    print(f"\nGenerated Django Secret Key:")
    print(generate_secret_key())
    print("(Save this for your environment variables)")
    
    setup_supabase_migration()
    setup_render_deployment()
    
    print("\nNext steps:")
    print("1. Set up Supabase database")
    print("2. Get database connection string")
    print("3. Deploy to Render with the connection string")
    print("4. Test API endpoints")
    print("5. Proceed with Lovable frontend setup")

if __name__ == "__main__":
    main()