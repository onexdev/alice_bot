“””
Configuration Module
Handles secure loading of API keys and configuration settings
“””

import json
import os
from pathlib import Path
from typing import Optional

class Config:
def **init**(self):
self.config_file = Path(“credentials/bscscan_key.json”)
self.api_key = None

```
def get_api_key(self) -> str:
    """
    Load BSCScan API key from secure credentials file
    """
    try:
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        api_key = config_data.get('bscscan_api_key')
        
        if not api_key:
            raise ValueError("API key not found in configuration file")
        
        if not self._validate_api_key(api_key):
            raise ValueError("Invalid API key format")
        
        self.api_key = api_key
        return api_key
        
    except FileNotFoundError as e:
        raise Exception(f"Configuration error: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON in configuration file: {str(e)}")
    except Exception as e:
        raise Exception(f"Configuration loading failed: {str(e)}")

def _validate_api_key(self, api_key: str) -> bool:
    """Validate API key format"""
    if not isinstance(api_key, str):
        return False
    
    # BSCScan API keys are typically 34 characters long
    if len(api_key) < 20:
        return False
    
    # Check if it contains only valid characters
    valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return all(c in valid_chars for c in api_key.upper())

def create_default_config(self):
    """Create default configuration file structure"""
    try:
        # Ensure credentials directory exists
        self.config_file.parent.mkdir(exist_ok=True)
        
        default_config = {
            "bscscan_api_key": "YOUR_API_KEY_HERE",
            "rate_limit": 5,
            "timeout": 30,
            "max_retries": 3
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
        
        return True
        
    except Exception as e:
        raise Exception(f"Failed to create default configuration: {str(e)}")

def get_setting(self, key: str, default=None):
    """Get specific setting from config"""
    try:
        if not self.config_file.exists():
            return default
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        return config_data.get(key, default)
        
    except Exception:
        return default
```
