#!/usr/bin/env python3
"""
ALICE Bot - API Key Setup Script
Helps configure and validate BSCScan API key
"""

import json
import requests
from pathlib import Path

def setup_api_key():
    """Setup and validate BSCScan API key"""
    print("🔑 ALICE Bot - API Key Setup")
    print("=" * 50)
    
    # Check if config file exists
    config_file = Path("credentials/bscscan_key.json")
    
    if config_file.exists():
        print("📁 Found existing configuration file")
        with open(config_file, 'r') as f:
            config = json.load(f)
        current_key = config.get('bscscan_api_key', '')
        
        if current_key and current_key != 'YourApiKeyHere':
            print(f"🔑 Current API Key: {current_key[:8]}...{current_key[-4:]}")
            
            choice = input("\nTest current API key? (y/n): ").lower().strip()
            if choice == 'y':
                if test_api_key(current_key):
                    print("✅ Current API key is working!")
                    return True
                else:
                    print("❌ Current API key failed test")
        else:
            print("⚠️ No valid API key found in configuration")
    else:
        print("📝 No configuration file found")
    
    # Get new API key
    print("\n🔗 Get your FREE BSCScan API key from:")
    print("   https://bscscan.com/apis")
    print("   1. Create account")
    print("   2. Go to API-KEYs")
    print("   3. Click 'Add' to create new API key")
    
    while True:
        api_key = input(f"\n🔑 Enter your BSCScan API key: ").strip()
        
        if not api_key:
            print("❌ API key cannot be empty")
            continue
        
        if len(api_key) < 20:
            print("❌ API key seems too short")
            continue
        
        print(f"\n🧪 Testing API key: {api_key[:8]}...{api_key[-4:]}")
        
        if test_api_key(api_key):
            print("✅ API key test successful!")
            
            # Save to config file
            config_file.parent.mkdir(exist_ok=True)
            
            config = {
                "bscscan_api_key": api_key,
                "rate_limit": 5,
                "timeout": 30,
                "max_retries": 3,
                "base_url": "https://api.bscscan.com/api"
            }
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            print(f"💾 API key saved to: {config_file}")
            print("\n🚀 You can now run ALICE Bot:")
            print("   python base.py sc WALLET_ADDRESS p Vv output.txt")
            
            return True
        else:
            print("❌ API key test failed")
            retry = input("Try another key? (y/n): ").lower().strip()
            if retry != 'y':
                break
    
    return False

def test_api_key(api_key: str) -> bool:
    """Test API key with a simple request"""
    try:
        url = "https://api.bscscan.com/api"
        params = {
            'module': 'stats',
            'action': 'bnbsupply',
            'apikey': api_key
        }
        
        print("📡 Sending test request...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
        
        data = response.json()
        
        if data.get('status') == '1':
            print("✅ API key is valid and working")
            return True
        else:
            error_msg = data.get('message', 'Unknown error')
            print(f"❌ API Error: {error_msg}")
            
            if 'invalid api key' in error_msg.lower():
                print("💡 Hint: Make sure you copied the API key correctly")
            elif 'rate limit' in error_msg.lower():
                print("💡 Hint: API key is valid but rate limited")
                return True  # Key is valid, just rate limited
            
            return False
            
    except requests.RequestException as e:
        print(f"❌ Network Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    if setup_api_key():
        print("\n🎉 Setup completed successfully!")
    else:
        print("\n❌ Setup failed. Please try again.")
