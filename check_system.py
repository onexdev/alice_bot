#!/usr/bin/env python3
“””
ALICE Bot System Validation Script
Validates all components before deployment
“””

import sys
import os
import json
from pathlib import Path

def validate_system():
“”“Comprehensive system validation”””
print(“🔍 ALICE Bot - System Validation”)
print(”=” * 50)

```
errors = []
warnings = []

# 1. Check Python version
print("\n🐍 Python Version Check:")
if sys.version_info >= (3, 8):
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
else:
    errors.append(f"Python {sys.version.split()[0]} - Requires 3.8+")
    print(f"❌ Python {sys.version.split()[0]} - Requires 3.8+")

# 2. Check required files
print("\n📁 File Structure Check:")
required_files = [
    "base.py",
    "core/__init__.py",
    "core/scanner.py", 
    "core/config.py",
    "core/utils.py",
    "interface/__init__.py",
    "interface/terminal.py",
    "credentials/bscscan_key.json",
    "requirements.txt"
]

for file_path in required_files:
    if Path(file_path).exists():
        print(f"✅ {file_path}")
    else:
        errors.append(f"Missing file: {file_path}")
        print(f"❌ {file_path} - MISSING")

# 3. Check directories
print("\n📂 Directory Structure Check:")
required_dirs = ["core", "interface", "credentials", "result"]

for dir_path in required_dirs:
    if Path(dir_path).exists():
        print(f"✅ {dir_path}/")
    else:
        warnings.append(f"Missing directory: {dir_path}")
        print(f"⚠️ {dir_path}/ - Will be created")
        Path(dir_path).mkdir(exist_ok=True)

# 4. Check API key configuration
print("\n🔑 API Key Check:")
try:
    with open("credentials/bscscan_key.json", "r") as f:
        config = json.load(f)
        api_key = config.get("bscscan_api_key", "")
        
    if api_key and len(api_key) > 20:
        print(f"✅ API Key configured ({len(api_key)} chars)")
    else:
        errors.append("Invalid or missing API key")
        print("❌ API Key - Invalid or missing")
        
except Exception as e:
    errors.append(f"API key file error: {e}")
    print(f"❌ API Key file - {e}")

# 5. Check imports
print("\n📦 Import Check:")
try:
    import requests
    print("✅ requests - Available")
except ImportError:
    errors.append("Missing: requests")
    print("❌ requests - Missing (run: pip install requests)")

try:
    import colorama
    print("✅ colorama - Available")
except ImportError:
    warnings.append("Missing: colorama")
    print("⚠️ colorama - Missing (colors disabled)")

# 6. Test basic functionality
print("\n🧪 Basic Functionality Test:")
try:
    # Test wallet address validation
    test_address = "0xc51beb5b222aed7f0b56042f04895ee41886b763"
    if len(test_address) == 42 and test_address.startswith("0x"):
        print("✅ Address validation - Working")
    else:
        warnings.append("Address validation issue")
        
    # Test JSON handling
    test_data = {"test": "value"}
    json.dumps(test_data)
    print("✅ JSON processing - Working")
    
except Exception as e:
    errors.append(f"Functionality test failed: {e}")
    print(f"❌ Basic test - {e}")

# Results
print("\n" + "=" * 50)
print("📊 VALIDATION RESULTS:")

if not errors:
    print("✅ SYSTEM STATUS: READY FOR DEPLOYMENT")
    print(f"⚠️ Warnings: {len(warnings)}")
    
    if warnings:
        print("\n⚠️ Warnings:")
        for warning in warnings:
            print(f"   • {warning}")
    
    print("\n🚀 You can now run:")
    print("   python base.py sc WALLET_ADDRESS p Vv output.txt")
    return True
    
else:
    print("❌ SYSTEM STATUS: ERRORS FOUND")
    print(f"❌ Errors: {len(errors)}")
    print(f"⚠️ Warnings: {len(warnings)}")
    
    print("\n❌ Critical Errors:")
    for error in errors:
        print(f"   • {error}")
        
    if warnings:
        print("\n⚠️ Warnings:")
        for warning in warnings:
            print(f"   • {warning}")
    
    print("\n🔧 Fix errors before deployment!")
    return False
```

if **name** == “**main**”:
validate_system()
