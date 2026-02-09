#!/usr/bin/env python3
"""
Alternative deployment approach for Render
"""

import os
import sys

def create_simple_build_script():
    """Create a simple build script for Render"""
    
    # Create a simple requirements file in root directory
    requirements_content = """Django==3.2.11
djangorestframework==3.13.1
django-cors-headers==3.11.0
drf-spectacular==0.21.1
django-ckeditor==6.2.0
django-filter==21.1
django-import-export==2.7.1
gunicorn==20.1.0
psycopg2-binary==2.9.5
whitenoise==6.2.0
django-environ==0.8.1
pillow==9.4.0
"""

    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    
    print("✅ Created requirements.txt in root directory")
    
    # Create build script
    build_script = """#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
"""
    
    with open("build.sh", "w") as f:
        f.write(build_script)
    
    # Make it executable on Unix systems
    if os.name != 'nt':  # Not Windows
        os.chmod("build.sh", 0o755)
    
    print("✅ Created build.sh script")
    
    print("\n📝 Update Render Configuration:")
    print("Build Command: bash build.sh")
    print("Start Command: gunicorn config.wsgi:application")

if __name__ == "__main__":
    create_simple_build_script()