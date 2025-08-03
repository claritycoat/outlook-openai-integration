#!/usr/bin/env python3
"""
Setup script for Outlook-OpenAI Integration
"""

import os
import subprocess
import sys

def install_dependencies():
    """Install required Python packages."""
    print("Installing required dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def create_env_file():
    """Create .env file from template."""
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping creation.")
        return True
    
    print("Creating .env file from template...")
    try:
        with open('env_example.txt', 'r') as template:
            content = template.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("✅ .env file created successfully")
        print("📝 Please edit the .env file with your actual credentials")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Outlook-OpenAI Integration")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your credentials")
    print("2. Set up Microsoft Azure App Registration")
    print("3. Get your OpenAI API key")
    print("4. Run: python outlook_openai_integration.py")
    print("\n📖 See README.md for detailed setup instructions")

if __name__ == "__main__":
    main() 