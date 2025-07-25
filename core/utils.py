"""
Utility Functions Module
Contains formatters, converters, and helper functions
"""

import re
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import hashlib
import json

class DataFormatter:
    """Data formatting utilities"""
    
    @staticmethod
    def format_wallet_address(address: str) -> str:
        """Format wallet address to standard format"""
        if not address:
            return "N/A"
        
        # Ensure address starts with 0x
        if not address.startswith('0x'):
            address = '0x' + address
        
        return address.lower()
    
    @staticmethod
    def format_token_amount(value: str, decimals: int = 18) -> str:
        """Format token amount from wei to readable format"""
        try:
            if not value or value == '0':
                return '0.000000'
            
            amount = int(value) / (10 ** decimals)
            return f"{amount:.6f}"
        except (ValueError, TypeError, ZeroDivisionError):
            return '0.000000'
    
    @staticmethod
    def format_timestamp(timestamp: str) -> str:
        """Format Unix timestamp to readable date"""
        try:
            ts = int(timestamp)
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except (ValueError, TypeError):
            return "Unknown"
    
    @staticmethod
    def calculate_age_precise(timestamp: str) -> str:
        """Calculate precise age from timestamp"""
        try:
            ts = int(timestamp)
            tx_time = datetime.fromtimestamp(ts, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            diff = now - tx_time
            
            total_seconds = int(diff.total_seconds())
            
            if total_seconds < 60:
                return f"{total_seconds}s ago"
            elif total_seconds < 3600:
                minutes = total_seconds // 60
                return f"{minutes}m ago"
            elif total_seconds < 86400:
                hours = total_seconds // 3600
                return f"{hours}h ago"
            else:
                days = total_seconds // 86400
                return f"{days}d ago"
        except (ValueError, TypeError):
            return "Unknown"

class AddressValidator:
    """Address validation utilities"""
    
    @staticmethod
    def is_valid_bsc_address(address: str) -> bool:
        """Validate BSC address format"""
        if not address or not isinstance(address, str):
            return False
        
        # Remove 0x prefix if present
        clean_address = address[2:] if address.startswith('0x') else address
        
        # Check length and hex format
        if len(clean_address) != 40:
            return False
        
        try:
            int(clean_address, 16)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_contract_address(address: str) -> bool:
        """Check if address is likely a contract (basic heuristic)"""
        if not AddressValidator.is_valid_bsc_address(address):
            return False
        
        # Simple heuristic: contracts often have more zeros or patterns
        clean_address = address[2:] if address.startswith('0x') else address
        zero_count = clean_address.count('0')
        
        # If more than 50% zeros, likely a contract
        return zero_count > 20

class DataFilter:
    """Data filtering and processing utilities"""
    
    @staticmethod
    def filter_unique_transactions(transactions: List[Dict]) -> List[Dict]:
        """Remove duplicate transactions based on hash"""
        seen_hashes = set()
        unique_transactions = []
        
        for tx in transactions:
            tx_hash = tx.get('hash', '')
            if tx_hash and tx_hash not in seen_hashes:
                seen_hashes.add(tx_hash)
                unique_transactions.append(tx)
        
        return unique_transactions
    
    @staticmethod
    def filter_by_method(transactions: List[Dict], methods: List[str]) -> List[Dict]:
        """Filter transactions by method type"""
        if not methods:
            return transactions
        
        filtered = []
        methods_lower = [m.lower() for m in methods]
        
        for tx in transactions:
            method = tx.get('method', '').lower()
            if method in methods_lower:
                filtered.append(tx)
        
        return filtered
    
    @staticmethod
    def filter_by_age(transactions: List[Dict], max_age_days: int) -> List[Dict]:
        """Filter transactions by maximum age"""
        if max_age_days <= 0:
            return transactions
        
        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 3600
        
        filtered = []
        for tx in transactions:
            try:
                timestamp = int(tx.get('timestamp', 0))
                if current_time - timestamp <= max_age_seconds:
                    filtered.append(tx)
            except (ValueError, TypeError):
                continue
        
        return filtered

class FileHandler:
    """File handling utilities"""
    
    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists"""
        try:
            from pathlib import Path
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def safe_filename(filename: str) -> str:
        """Generate safe filename"""
        # Remove or replace unsafe characters
        safe_chars = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Limit length
        if len(safe_chars) > 100:
            safe_chars = safe_chars[:100]
        
        return safe_chars
    
    @staticmethod
    def generate_unique_filename(base_name: str, extension: str = 'txt') -> str:
        """Generate unique filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}_{timestamp}.{extension}"

class PerformanceMonitor:
    """Performance monitoring utilities"""
    
    def __init__(self):
        self.start_time = None
        self.checkpoints = {}
    
    def start(self):
        """Start performance monitoring"""
        self.start_time = time.time()
        return self.start_time
    
    def checkpoint(self, name: str) -> float:
        """Add performance checkpoint"""
        if not self.start_time:
            self.start()
        
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.checkpoints[name] = elapsed
        return elapsed
    
    def get_elapsed(self) -> float:
        """Get total elapsed time"""
        if not self.start_time:
            return 0.0
        return time.time() - self.start_time
    
    def get_report(self) -> Dict[str, float]:
        """Get performance report"""
        report = {
            'total_elapsed': self.get_elapsed(),
            'checkpoints': self.checkpoints.copy()
        }
        return report

class SecurityUtils:
    """Security-related utilities"""
    
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """Sanitize user input"""
        if not isinstance(input_str, str):
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\';\\]', '', input_str)
        
        # Limit length
        if len(sanitized) > 1000:
            sanitized = sanitized[:1000]
        
        return sanitized.strip()
    
    @staticmethod
    def hash_address(address: str) -> str:
        """Generate hash of address for privacy"""
        if not address:
            return ""
        
        return hashlib.sha256(address.encode()).hexdigest()[:16]
    
    @staticmethod
    def mask_sensitive_data(data: str, visible_chars: int = 6) -> str:
        """Mask sensitive data showing only first and last few characters"""
        if not data or len(data) <= visible_chars * 2:
            return data
        
        visible = visible_chars
        return f"{data[:visible]}...{data[-visible:]}"

class JsonUtils:
    """JSON handling utilities"""
    
    @staticmethod
    def safe_json_load(file_path: str) -> Optional[Dict]:
        """Safely load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, Exception):
            return None
    
    @staticmethod
    def safe_json_save(data: Dict, file_path: str) -> bool:
        """Safely save data to JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

class ErrorHandler:
    """Error handling utilities"""
    
    @staticmethod
    def categorize_error(error: Exception) -> str:
        """Categorize error type"""
        error_type = type(error).__name__
        error_msg = str(error).lower()
        
        if 'network' in error_msg or 'connection' in error_msg:
            return 'NETWORK_ERROR'
        elif 'timeout' in error_msg:
            return 'TIMEOUT_ERROR'
        elif 'api' in error_msg or 'rate limit' in error_msg:
            return 'API_ERROR'
        elif 'permission' in error_msg or 'access' in error_msg:
            return 'PERMISSION_ERROR'
        elif 'file' in error_msg or 'directory' in error_msg:
            return 'FILE_ERROR'
        else:
            return 'UNKNOWN_ERROR'
    
    @staticmethod
    def get_error_suggestion(error_category: str) -> str:
        """Get suggestion for error resolution"""
        suggestions = {
            'NETWORK_ERROR': 'Check internet connection and try again',
            'TIMEOUT_ERROR': 'Increase timeout value or try again later',
            'API_ERROR': 'Check API key validity and rate limits',
            'PERMISSION_ERROR': 'Check file permissions and access rights',
            'FILE_ERROR': 'Verify file paths and directory structure',
            'UNKNOWN_ERROR': 'Contact support with error details'
        }
        
        return suggestions.get(error_category, 'Unknown error occurred')
