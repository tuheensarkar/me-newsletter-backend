#!/usr/bin/env python3
"""
Automated Deployment Script for ME Newsletter Migration
"""

import os
import subprocess
import sys
import time
from pathlib import Path

def print_step(step_num, description):
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {description}")
    print('='*60)

def run_command(command, cwd=None, description=""):
    """Run a command and handle errors"""
    try:
        print(f"Executing: {command}")
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Failed")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return False

def step_1_setup_database():
    """Step 1: Set up Supabase database"""
    print_step(1, "Set up Supabase Database")
    
    print("Please follow these steps manually:")
    print("1. Go to https://supabase.com")
    print("2. Create a free account")
    print("3. Create a new project")
    print("4. Note your database connection string")
    print("5. Save the connection string for later use")
    
    input("Press Enter when you have completed these steps...")

def step_2_deploy_backend():
    """Step 2: Deploy Django backend to Render"""
    print_step(2, "Deploy Backend to Render")
    
    print("Please follow these steps:")
    print("1. Go to https://render.com")
    print("2. Create a free account")
    print("3. Click 'New Web Service'")
    print("4. Connect your GitHub repository")
    print("5. Use these settings:")
    print("   - Name: me-newsletter-backend")
    print("   - Runtime: Python 3")
    print("   - Build Command: pip install -r requirements/production.txt")
    print("   - Start Command: gunicorn config.wsgi:application")
    
    print("\nEnvironment Variables to add:")
    print("DATABASE_URL=your-supabase-connection-string")
    print("DJANGO_SECRET_KEY=BQt#=u_@:b$*ArP>V/KK>S&HARV3+F+Zkkgw~=fQmxpGC_H&m=")
    print("DJANGO_DEBUG=False")
    print("DJANGO_ALLOWED_HOSTS=*")
    
    input("Press Enter when backend is deployed...")

def step_3_test_backend():
    """Step 3: Test backend deployment"""
    print_step(3, "Test Backend Deployment")
    
    backend_url = input("Enter your Render backend URL (e.g., https://me-newsletter-backend.onrender.com): ")
    
    test_commands = [
        f"curl {backend_url}/api/status/",
        f"curl {backend_url}/api/health/",
        f"curl {backend_url}/api/v1/newsletters/"
    ]
    
    for cmd in test_commands:
        print(f"Testing: {cmd}")
        run_command(cmd)
        time.sleep(1)

def step_4_install_frontend_deps():
    """Step 4: Install frontend dependencies"""
    print_step(4, "Install Frontend Dependencies")
    
    frontend_dir = "../newsletter-frontend"
    
    if run_command("npm install", cwd=frontend_dir, description="Installing dependencies"):
        print("✅ Frontend dependencies installed")

def step_5_configure_frontend():
    """Step 5: Configure frontend environment"""
    print_step(5, "Configure Frontend Environment")
    
    backend_url = input("Enter your backend API URL: ")
    
    env_content = f"""# Environment Variables for Newsletter Frontend

# API Configuration
NEXT_PUBLIC_API_URL={backend_url}/api/v1

# Development
NODE_ENV=development

# Build Configuration
NEXT_TELEMETRY_DISABLED=1
"""
    
    env_file = "../newsletter-frontend/.env.local"
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print("✅ Environment file created")

def step_6_test_frontend_local():
    """Step 6: Test frontend locally"""
    print_step(6, "Test Frontend Locally")
    
    frontend_dir = "../newsletter-frontend"
    
    print("Starting local development server...")
    print("Navigate to http://localhost:3000 to test")
    
    try:
        subprocess.run("npm run dev", shell=True, cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\nDevelopment server stopped")

def step_7_deploy_frontend_lovable():
    """Step 7: Deploy to Lovable"""
    print_step(7, "Deploy Frontend to Lovable")
    
    print("Manual deployment steps:")
    print("1. Go to https://lovable.dev")
    print("2. Create account and new project")
    print("3. Connect your GitHub repository")
    print("4. Set environment variable:")
    print("   NEXT_PUBLIC_API_URL=your-backend-url/api/v1")
    print("5. Deploy and test")

def main():
    print("🚀 ME Newsletter Migration Automation")
    print("="*50)
    
    steps = [
        step_1_setup_database,
        step_2_deploy_backend,
        step_3_test_backend,
        step_4_install_frontend_deps,
        step_5_configure_frontend,
        step_6_test_frontend_local,
        step_7_deploy_frontend_lovable
    ]
    
    for i, step_func in enumerate(steps, 1):
        try:
            step_func()
            
            if i < len(steps):
                continue_choice = input(f"\nContinue to step {i+1}? (y/n): ")
                if continue_choice.lower() != 'y':
                    break
                    
        except KeyboardInterrupt:
            print("\n\nMigration interrupted by user")
            break
        except Exception as e:
            print(f"Error in step {i}: {e}")
            retry = input("Retry this step? (y/n): ")
            if retry.lower() == 'y':
                step_func()
    
    print("\n" + "="*50)
    print("🎉 Migration Process Completed!")
    print("="*50)
    print("Next steps:")
    print("1. Monitor your deployments")
    print("2. Test all functionality")
    print("3. Update DNS if needed")
    print("4. Set up monitoring and analytics")

if __name__ == "__main__":
    main()