#!/usr/bin/env python3
"""
Quick Deployment Fix Script
"""

import os
import subprocess

def fix_render_deployment():
    """Fix common Render deployment issues"""
    
    print("🔧 Fixing Render Deployment Issues...")
    
    # Check if requirements/production.txt exists
    if not os.path.exists("requirements/production.txt"):
        print("Creating requirements/production.txt...")
        with open("requirements/base.txt", "r") as base_file:
            base_content = base_file.read()
        
        production_content = base_content + "\n# Production dependencies\ngunicorn==20.1.0\npsycopg2-binary==2.9.5\nwhitenoise==6.2.0\n"
        
        with open("requirements/production.txt", "w") as prod_file:
            prod_file.write(production_content)
        print("✅ requirements/production.txt created")
    
    # Check if runtime.txt exists
    if not os.path.exists("runtime.txt"):
        print("Creating runtime.txt...")
        with open("runtime.txt", "w") as runtime_file:
            runtime_file.write("python-3.13.2")
        print("✅ runtime.txt created")
    
    # Check if render.yaml exists
    if not os.path.exists("render.yaml"):
        render_config = """services:
  - type: web
    name: me-newsletter-backend
    env: python
    buildCommand: "pip install -r requirements/production.txt"
    startCommand: "gunicorn config.wsgi:application"
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: DJANGO_SECRET_KEY
        sync: false
      - key: DJANGO_DEBUG
        value: False
      - key: DJANGO_ALLOWED_HOSTS
        value: "*"
"""
        with open("render.yaml", "w") as render_file:
            render_file.write(render_config)
        print("✅ render.yaml created")
    
    print("\n📋 Next Steps:")
    print("1. Commit these changes to your GitHub repository")
    print("2. Redeploy on Render")
    print("3. Add these environment variables in Render dashboard:")
    print("   - DATABASE_URL (your Supabase connection string)")
    print("   - DJANGO_SECRET_KEY (BQt#=u_@:b$*ArP>V/KK>S&HARV3+F+Zkkgw~=fQmxpGC_H&m=)")
    print("   - DJANGO_DEBUG=False")
    print("   - DJANGO_ALLOWED_HOSTS=your-render-app-url.onrender.com")

if __name__ == "__main__":
    fix_render_deployment()