"""
1
Terminal Interface Module
Handles all terminal output, debugging, and visual elements
"""

import os
import sys
from datetime import datetime

class TerminalInterface:
    def __init__(self):
        # Initialize colorama for Windows compatibility
        try:
            import colorama
            colorama.init()
            self.colors = {
                'RESET': '\033[0m',
                'RED': '\033[91m',
                'GREEN': '\033[92m',
                'YELLOW': '\033[93m',
                'BLUE': '\033[94m',
                'MAGENTA': '\033[95m',
                'CYAN': '\033[96m',
                'WHITE': '\033[97m',
                'BOLD': '\033[1m',
                'DIM': '\033[2m',
                'UNDERLINE': '\033[4m'
            }
        except ImportError:
            # Fallback if colorama not available
            self.colors = {key: '' for key in [
                'RESET', 'RED', 'GREEN', 'YELLOW', 'BLUE', 
                'MAGENTA', 'CYAN', 'WHITE', 'BOLD', 'DIM', 'UNDERLINE'
            ]}
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_timestamp(self):
        """Get formatted timestamp"""
        return datetime.now().strftime("%H:%M:%S")
    
    def show_welcome(self):
        """Display professional welcome screen"""
        self.clear_screen()
        
        print(f"{self.colors['CYAN']}{self.colors['BOLD']}")
        print("╔" + "="*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "🤖 ALICE - Advanced BSC Scanner Bot".center(78) + "║")
        print("║" + "Intelligent Transaction Analysis System".center(78) + "║")
        print("║" + " "*78 + "║")
        print("║" + f"Author: onex_dv".center(78) + "║")
        print("║" + f"GitHub: https://github.com/onexdev".center(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "="*78 + "╝")
        print(f"{self.colors['RESET']}")
        
        print(f"{self.colors['YELLOW']}")
        print("📋 DOKUMENTASI KRITIS BOT:")
        print("├─ Bot ini dirancang untuk mengambil data transaksi BSC dengan efisiensi tinggi")
        print("├─ Menggunakan algoritma optimized untuk eksekusi < 1 detik per request")
        print("├─ Dilengkapi sistem debugging kritis untuk monitoring real-time")
        print("├─ Output tersedia dalam 2 format: Full data dan wallet addresses only")
        print("├─ Implementasi error handling komprehensif untuk stabilitas maksimal")
        print("└─ Rate limiting otomatis untuk compliance dengan BSCScan API")
        print(f"{self.colors['RESET']}")
        
        print(f"{self.colors['GREEN']}Status: {self.colors['BOLD']}READY TO SCAN{self.colors['RESET']}")
        print(f"{self.colors['BLUE']}System: {self.colors['BOLD']}ALICE v1.0 - Production Ready{self.colors['RESET']}")
    
    def show_goodbye(self):
        """Display goodbye message"""
        print(f"\n{self.colors['MAGENTA']}")
        print("╔" + "="*40 + "╗")
        print("║" + "See you next time! onex_dv".center(40) + "║")
        print("╚" + "="*40 + "╝")
        print(f"{self.colors['RESET']}")
    
    def debug_step(self, category, message):
        """Display debug step information"""
        timestamp = self.get_timestamp()
        print(f"{self.colors['BLUE']}[{timestamp}] {self.colors['BOLD']}[{category}]{self.colors['RESET']} {self.colors['WHITE']}→ {message}{self.colors['RESET']}")
    
    def debug_success(self, category, message):
        """Display success debug information"""
        timestamp = self.get_timestamp()
        print(f"{self.colors['GREEN']}[{timestamp}] {self.colors['BOLD']}[{category}]{self.colors['RESET']} {self.colors['GREEN']}✓ {message}{self.colors['RESET']}")
    
    def debug_error(self, category, message):
        """Display error debug information"""
        timestamp = self.get_timestamp()
        print(f"{self.colors['RED']}[{timestamp}] {self.colors['BOLD']}[{category}]{self.colors['RESET']} {self.colors['RED']}✗ ERROR: {message}{self.colors['RESET']}")
    
    def debug_warning(self, category, message):
        """Display warning debug information"""
        timestamp = self.get_timestamp()
        print(f"{self.colors['YELLOW']}[{timestamp}] {self.colors['BOLD']}[{category}]{self.colors['RESET']} {self.colors['YELLOW']}⚠ WARNING: {message}{self.colors['RESET']}")
    
    def debug_info(self, category, message):
        """Display info debug information"""
        timestamp = self.get_timestamp()
        print(f"{self.colors['CYAN']}[{timestamp}] {self.colors['BOLD']}[{category}]{self.colors['RESET']} {self.colors['CYAN']}ℹ {message}{self.colors['RESET']}")
    
    def debug_data(self, category, message):
        """Display data debug information"""
        timestamp = self.get_timestamp()
        print(f"{self.colors['MAGENTA']}[{timestamp}] {self.colors['BOLD']}[{category}]{self.colors['RESET']} {self.colors['MAGENTA']}📊 {message}{self.colors['RESET']}")
    
    def debug_api(self, category, message):
        """Display API debug information"""
        timestamp = self.get_timestamp()
        print(f"{self.colors['CYAN']}[{timestamp}] {self.colors['BOLD']}[{category}]{self.colors['RESET']} {self.colors['CYAN']}📡 {message}{self.colors['RESET']}")
    
    def debug_progress(self, current, total, message="Processing"):
        """Display progress information"""
        percentage = (current / total) * 100 if total > 0 else 0
        filled = int(percentage // 2)
        bar = "█" * filled + "░" * (50 - filled)
        
        print(f"\r{self.colors['GREEN']}[PROGRESS] {bar} {percentage:.1f}% ({current}/{total}) {message}{self.colors['RESET']}", end="")
        
        if current == total:
            print()  # New line when complete
    
    def display_critical_error(self, error_type, error_message, solution=None):
        """Display critical error with detailed information"""
        print(f"\n{self.colors['RED']}{self.colors['BOLD']}")
        print("╔" + "="*60 + "╗")
        print("║" + f"CRITICAL ERROR DETECTED".center(60) + "║")
        print("╠" + "="*60 + "╣")
        print("║" + f"Type: {error_type}".ljust(60) + "║")
        print("║" + f"Message: {error_message}"[:58].ljust(60) + "║")
        if solution:
            print("║" + "Solution:".ljust(60) + "║")
            print("║" + f"  {solution}"[:58].ljust(60) + "║")
        print("╚" + "="*60 + "╝")
        print(f"{self.colors['RESET']}")
    
    def display_api_stats(self, requests_made, rate_limit, remaining):
        """Display API usage statistics"""
        print(f"\n{self.colors['YELLOW']}API Usage Statistics:")
        print(f"├─ Requests Made: {requests_made}")
        print(f"├─ Rate Limit: {rate_limit}/second")
        print(f"└─ Remaining: {remaining}{self.colors['RESET']}")
