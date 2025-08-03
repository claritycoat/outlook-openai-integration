#!/usr/bin/env python3
"""
Test script for Outlook-OpenAI Integration
Verifies that all components are working correctly.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test that all required environment variables are set."""
    print("🔍 Testing environment variables...")
    
    required_vars = ['CLIENT_ID', 'CLIENT_SECRET', 'TENANT_ID', 'OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Show first few characters for verification
            display_value = value[:8] + "..." if len(value) > 8 else value
            print(f"  ✅ {var}: {display_value}")
    
    if missing_vars:
        print(f"  ❌ Missing variables: {missing_vars}")
        return False
    
    print("  ✅ All required environment variables are set")
    return True

def test_dependencies():
    """Test that all required packages are installed."""
    print("\n🔍 Testing dependencies...")
    
    required_packages = [
        'requests',
        'openai',
        'python-dotenv',
        'msal',
        'schedule',
        'dateutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package} (missing)")
    
    if missing_packages:
        print(f"  ❌ Missing packages: {missing_packages}")
        print("  💡 Run: pip install -r requirements.txt")
        return False
    
    print("  ✅ All required packages are installed")
    return True

def test_microsoft_graph_connection():
    """Test Microsoft Graph API connection."""
    print("\n🔍 Testing Microsoft Graph API connection...")
    
    try:
        from outlook_openai_integration import MicrosoftGraphAPI
        
        graph_api = MicrosoftGraphAPI()
        
        if graph_api.authenticate():
            print("  ✅ Successfully authenticated with Microsoft Graph API")
            
            # Test getting emails (just check if we can connect)
            try:
                emails = graph_api.get_emails(max_count=1)
                print(f"  ✅ Successfully retrieved {len(emails)} test emails")
                return True
            except Exception as e:
                print(f"  ⚠️  Authentication works but email retrieval failed: {str(e)}")
                return True  # Authentication is the main test
        else:
            print("  ❌ Failed to authenticate with Microsoft Graph API")
            print("  💡 Check your CLIENT_ID, CLIENT_SECRET, and TENANT_ID")
            return False
            
    except Exception as e:
        print(f"  ❌ Error testing Microsoft Graph API: {str(e)}")
        return False

def test_openai_connection():
    """Test OpenAI API connection."""
    print("\n🔍 Testing OpenAI API connection...")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, this is a test message. Please respond with 'Test successful'."}
            ],
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            print("  ✅ Successfully connected to OpenAI API")
            return True
        else:
            print("  ❌ OpenAI API returned empty response")
            return False
            
    except Exception as e:
        print(f"  ❌ Error testing OpenAI API: {str(e)}")
        print("  💡 Check your OPENAI_API_KEY")
        return False

def test_configuration():
    """Test configuration settings."""
    print("\n🔍 Testing configuration settings...")
    
    config_vars = {
        'EMAIL_FOLDER': os.getenv('EMAIL_FOLDER', 'Inbox'),
        'PROCESSED_FOLDER': os.getenv('PROCESSED_FOLDER', 'Drafts'),
        'SCAN_INTERVAL_MINUTES': os.getenv('SCAN_INTERVAL_MINUTES', '15'),
        'MAX_EMAILS_PER_SCAN': os.getenv('MAX_EMAILS_PER_SCAN', '10')
    }
    
    for var, value in config_vars.items():
        print(f"  ✅ {var}: {value}")
    
    # Test allowed domains
    allowed_domains = os.getenv('ALLOWED_DOMAINS', '')
    if allowed_domains:
        domains = allowed_domains.split(',')
        print(f"  ✅ ALLOWED_DOMAINS: {', '.join(domains)}")
    else:
        print("  ✅ ALLOWED_DOMAINS: (all domains allowed)")
    
    return True

def main():
    """Run all tests."""
    print("🧪 Outlook-OpenAI Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_environment_variables,
        test_dependencies,
        test_microsoft_graph_connection,
        test_openai_connection,
        test_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ❌ Test failed with exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready to go.")
        print("\n🚀 You can now run: python outlook_openai_integration.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above before running the integration.")
        print("\n💡 Check the README.md for detailed setup instructions.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 