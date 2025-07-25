"""
BSC Scanner Core Module
Handles all BSCScan API interactions with optimized performance
"""

import requests
import time
import json
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import asyncio
import aiohttp
import concurrent.futures
from threading import Lock

class BSCScanner:
    def __init__(self, api_key: str, terminal_interface):
        self.api_key = api_key
        self.terminal = terminal_interface
        self.base_url = "https://api.bscscan.com/api"
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(5)  # 5 requests per second
        self.request_count = 0
        self.lock = Lock()
        
        # Configure session for optimal performance
        self.session.headers.update({
            'User-Agent': 'ALICE-Bot/1.0 (BSC Scanner)',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        
        # Session pool for connection reuse
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=3
        )
        self.session.mount('https://', adapter)
    
    def scan_wallet_transactions(self, wallet_address: str) -> List[Dict[str, Any]]:
        """
        Scan wallet for token transfer transactions with optimized performance
        """
        try:
            self.terminal.debug_step("SCAN", f"Initiating scan for wallet: {wallet_address}")
            self.terminal.debug_step("VALIDATION", "Validating wallet address format")
            
            if not self._validate_wallet_address(wallet_address):
                raise ValueError("Invalid wallet address format")
            
            self.terminal.debug_success("VALIDATION", "Wallet address format valid")
            
            # Get token transfer transactions
            self.terminal.debug_step("API", "Fetching token transfer transactions")
            transactions = self._get_token_transfers(wallet_address)
            
            if not transactions:
                self.terminal.debug_warning("API", "No token transfer transactions found")
                return []
            
            self.terminal.debug_success("API", f"Retrieved {len(transactions)} raw transactions")
            
            # Process transactions with optimization
            self.terminal.debug_step("PROCESS", "Processing transaction data")
            processed_transactions = self._process_transactions(transactions)
            
            self.terminal.debug_success("PROCESS", f"Processed {len(processed_transactions)} transactions")
            
            return processed_transactions
            
        except Exception as e:
            self.terminal.debug_error("SCAN", f"Scan failed: {str(e)}")
            self._handle_critical_error("SCAN_ERROR", str(e))
            return []
    
    def _validate_wallet_address(self, address: str) -> bool:
        """Validate BSC wallet address format"""
        if not address or not isinstance(address, str):
            return False
        
        # Remove '0x' prefix if present
        if address.startswith('0x'):
            address = address[2:]
        
        # Check if it's 40 hex characters
        if len(address) != 40:
            return False
        
        try:
            int(address, 16)
            return True
        except ValueError:
            return False
    
    def _get_token_transfers(self, wallet_address: str) -> List[Dict]:
        """Get token transfer transactions with rate limiting"""
        try:
            # Apply rate limiting
            self.rate_limiter.wait()
            
            params = {
                'module': 'account',
                'action': 'tokentx',
                'address': wallet_address,
                'startblock': 0,
                'endblock': 999999999,
                'page': 1,
                'offset': 1000,  # Maximum allowed
                'sort': 'desc',
                'apikey': self.api_key
            }
            
            self.terminal.debug_api("REQUEST", f"Sending API request to BSCScan")
            
            with self.lock:
                self.request_count += 1
            
            start_time = time.time()
            response = self.session.get(self.base_url, params=params, timeout=30)
            execution_time = time.time() - start_time
            
            self.terminal.debug_api("RESPONSE", f"API response received in {execution_time:.3f}s")
            
            if response.status_code != 200:
                raise requests.RequestException(f"HTTP {response.status_code}: {response.text}")
            
            data = response.json()
            
            if data.get('status') != '1':
                error_msg = data.get('message', 'Unknown API error')
                if 'rate limit' in error_msg.lower():
                    self.terminal.debug_warning("API", "Rate limit detected, implementing backoff")
                    time.sleep(1)
                    return self._get_token_transfers(wallet_address)  # Retry
                raise Exception(f"BSCScan API Error: {error_msg}")
            
            transactions = data.get('result', [])
            self.terminal.debug_success("API", f"Retrieved {len(transactions)} token transfers")
            
            return transactions
            
        except requests.RequestException as e:
            self.terminal.debug_error("API", f"Network error: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            self.terminal.debug_error("API", f"JSON decode error: {str(e)}")
            raise
        except Exception as e:
            self.terminal.debug_error("API", f"Unexpected error: {str(e)}")
            raise
    
    def _process_transactions(self, raw_transactions: List[Dict]) -> List[Dict[str, Any]]:
        """
        Process raw transactions into structured format with high performance
        """
        processed = []
        total = len(raw_transactions)
        
        self.terminal.debug_step("PROCESS", f"Processing {total} transactions")
        
        for i, tx in enumerate(raw_transactions):
            try:
                # Show progress for large datasets
                if i % 100 == 0 or i == total - 1:
                    self.terminal.debug_progress(i + 1, total, "Processing transactions")
                
                processed_tx = {
                    'hash': tx.get('hash', 'N/A'),
                    'method': self._extract_method(tx),
                    'age': self._calculate_age(tx.get('timeStamp', '0')),
                    'from': tx.get('from', 'N/A').lower(),
                    'to': tx.get('to', 'N/A').lower(),
                    'token': self._format_token_info(tx)
                }
                
                processed.append(processed_tx)
                
            except Exception as e:
                self.terminal.debug_warning("PROCESS", f"Failed to process transaction {i}: {str(e)}")
                continue
        
        # Filter out duplicates based on hash
        unique_transactions = []
        seen_hashes = set()
        
        for tx in processed:
            if tx['hash'] not in seen_hashes:
                unique_transactions.append(tx)
                seen_hashes.add(tx['hash'])
        
        self.terminal.debug_success("PROCESS", f"Filtered to {len(unique_transactions)} unique transactions")
        
        return unique_transactions
    
    def _extract_method(self, tx: Dict) -> str:
        """Extract transaction method/function name"""
        # For token transfers, the method is typically 'transfer'
        if tx.get('functionName'):
            return tx.get('functionName', 'transfer')
        
        # Check input data for method signature
        input_data = tx.get('input', '')
        if input_data and len(input_data) >= 10:
            method_sig = input_data[:10]
            # Common method signatures
            method_map = {
                '0xa9059cbb': 'transfer',
                '0x23b872dd': 'transferFrom',
                '0x095ea7b3': 'approve',
                '0xa0712d68': 'mint',
                '0x42966c68': 'burn'
            }
            return method_map.get(method_sig, 'unknown')
        
        return 'transfer'  # Default for token transfers
    
    def _calculate_age(self, timestamp_str: str) -> str:
        """Calculate transaction age from timestamp"""
        try:
            timestamp = int(timestamp_str)
            tx_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            diff = now - tx_time
            
            if diff.days > 0:
                return f"{diff.days} days ago"
            elif diff.seconds > 3600:
                hours = diff.seconds // 3600
                return f"{hours} hours ago"
            elif diff.seconds > 60:
                minutes = diff.seconds // 60
                return f"{minutes} minutes ago"
            else:
                return "Just now"
                
        except (ValueError, TypeError):
            return "Unknown"
    
    def _format_token_info(self, tx: Dict) -> str:
        """Format token information"""
        token_name = tx.get('tokenName', 'Unknown')
        token_symbol = tx.get('tokenSymbol', 'UNK')
        value = tx.get('value', '0')
        decimals = int(tx.get('tokenDecimal', '18'))
        
        try:
            # Convert value from wei to token units
            token_value = int(value) / (10 ** decimals)
            return f"{token_value:.6f} {token_symbol} ({token_name})"
        except (ValueError, TypeError, ZeroDivisionError):
            return f"{token_symbol} ({token_name})"
    
    def _handle_critical_error(self, error_type: str, error_message: str):
        """Handle critical errors with detailed logging"""
        solutions = {
            'SCAN_ERROR': 'Check wallet address format and API key validity',
            'API_ERROR': 'Verify API key and check BSCScan service status',
            'NETWORK_ERROR': 'Check internet connection and try again',
            'RATE_LIMIT': 'Wait for rate limit reset or upgrade API plan'
        }
        
        solution = solutions.get(error_type, 'Contact support for assistance')
        self.terminal.display_critical_error(error_type, error_message, solution)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scanner statistics"""
        return {
            'requests_made': self.request_count,
            'rate_limit': self.rate_limiter.limit,
            'session_active': True
        }

class RateLimiter:
    """Rate limiter for API requests"""
    
    def __init__(self, requests_per_second: int):
        self.limit = requests_per_second
        self.requests = []
        self.lock = Lock()
    
    def wait(self):
        """Wait if necessary to respect rate limit"""
        with self.lock:
            now = time.time()
            
            # Remove requests older than 1 second
            self.requests = [req_time for req_time in self.requests if now - req_time < 1.0]
            
            # If we're at the limit, wait
            if len(self.requests) >= self.limit:
                sleep_time = 1.0 - (now - self.requests[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    self.wait()  # Recursive call to recheck
                    return
            
            # Add current request
            self.requests.append(now)
