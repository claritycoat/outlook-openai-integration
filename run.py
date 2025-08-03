#!/usr/bin/env python3
"""
Launcher script for Outlook-OpenAI Integration
"""

import sys
import subprocess
import os

def show_menu():
    """Display the main menu."""
    print("🚀 Outlook-OpenAI Integration Launcher")
    print("=" * 40)
    print("1. Test Setup")
    print("2. Run Integration")
    print("3. Install Dependencies")
    print("4. View Logs")
    print("5. Exit")
    print("=" * 40)

def test_setup():
    """Run the test setup script."""
    print("🧪 Running setup tests...")
    try:
        result = subprocess.run([sys.executable, "test_setup.py"], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def run_integration():
    """Run the main integration."""
    print("🚀 Starting Outlook-OpenAI Integration...")
    print("Press Ctrl+C to stop")
    try:
        subprocess.run([sys.executable, "outlook_openai_integration.py"])
    except KeyboardInterrupt:
        print("\n⏹️  Integration stopped by user")

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def view_logs():
    """View the log file."""
    log_file = "outlook_openai.log"
    if os.path.exists(log_file):
        print(f"📋 Recent logs from {log_file}:")
        print("-" * 50)
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                # Show last 20 lines
                for line in lines[-20:]:
                    print(line.rstrip())
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
    else:
        print("📋 No log file found yet. Run the integration first to generate logs.")

def main():
    """Main launcher function."""
    while True:
        show_menu()
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            test_setup()
        elif choice == "2":
            run_integration()
        elif choice == "3":
            install_dependencies()
        elif choice == "4":
            view_logs()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please select 1-5.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 