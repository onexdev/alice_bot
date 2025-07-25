#!/usr/bin/env python3
"""
ALICE Bot - Advanced BSC Scanner
Author: onex_dv
GitHub: https://github.com/onexdev
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from interface.terminal import TerminalInterface
from core.scanner import BSCScanner
from core.config import Config

class AliceBot:
    def __init__(self):
        self.terminal = TerminalInterface()
        self.config = Config()
        self.scanner = None
        
    def initialize(self):
        """Initialize bot components with critical debugging"""
        try:
            self.terminal.debug_step("INIT", "Loading configuration")
            api_key = self.config.get_api_key()
            
            self.terminal.debug_step("INIT", "Initializing BSC Scanner")
            self.scanner = BSCScanner(api_key, self.terminal)
            
            self.terminal.debug_success("INIT", "Bot initialized successfully")
            return True
            
        except Exception as e:
            self.terminal.debug_error("INIT", f"Failed to initialize: {str(e)}")
            return False
    
    def show_welcome(self):
        """Display professional welcome screen"""
        self.terminal.show_welcome()
        
    def show_help(self):
        """Display help information"""
        help_text = """
ALICE Bot - Command Usage:

Format: base.py <command> <wallet_address> <action> <version> <output_file>

Commands:
  sc, scan     - Start wallet scanning
  h, help      - Show this help

Actions:
  p, print     - Print results to file

Versions:
  Vv          - Full version (hash + method + age + from + to + token)
  Vf          - From version (only wallet addresses)

Examples:
  base.py sc 0xc51beb5b222aed7f0b56042f04895ee41886b763 p Vv wallet.txt
  base.py sc 0xc51beb5b222aed7f0b56042f04895ee41886b763 p Vf wallet.txt
  base.py help
        """
        print(help_text)
    
    def confirm_scan(self):
        """Get user confirmation to start scanning"""
        while True:
            try:
                choice = input(f"\n{self.terminal.colors['YELLOW']}Scan sekarang/keluar (y/n): {self.terminal.colors['RESET']}").lower().strip()
                
                if choice in ['y', 'yes']:
                    return True
                elif choice in ['n', 'no']:
                    self.terminal.show_goodbye()
                    return False
                else:
                    self.terminal.debug_warning("INPUT", "Please enter 'y' or 'n'")
                    
            except KeyboardInterrupt:
                self.terminal.show_goodbye()
                return False
    
    def run_scan(self, wallet_address, version, output_file):
        """Execute the scanning process"""
        try:
            self.terminal.debug_step("SCAN", f"Starting scan for wallet: {wallet_address}")
            self.terminal.debug_step("SCAN", f"Output version: {version}")
            self.terminal.debug_step("SCAN", f"Output file: {output_file}")
            
            # Execute scan
            transactions = self.scanner.scan_wallet_transactions(wallet_address)
            
            if not transactions:
                self.terminal.debug_warning("SCAN", "No transactions found")
                return False
            
            # Process and save results
            self.terminal.debug_step("SAVE", "Processing transaction data")
            
            # Ensure result directory exists
            result_dir = Path("result")
            result_dir.mkdir(exist_ok=True)
            
            output_path = result_dir / output_file
            
            if version.lower() == 'vv':
                self.save_full_version(transactions, output_path)
            elif version.lower() == 'vf':
                self.save_from_version(transactions, output_path)
            else:
                self.terminal.debug_error("SAVE", f"Invalid version: {version}")
                return False
            
            # Success message
            total_count = len(transactions)
            self.terminal.debug_success("COMPLETE", f"Scan completed successfully!")
            self.terminal.debug_info("RESULT", f"Total transactions processed: {total_count}")
            self.terminal.debug_info("RESULT", f"File saved to: result/{output_file}")
            
            print(f"\n{self.terminal.colors['GREEN']}{'='*60}")
            print(f"🎉 SCAN COMPLETED SUCCESSFULLY! 🎉")
            print(f"Total wallet addresses found: {total_count}")
            print(f"Results saved to: result/{output_file}")
            print(f"{'='*60}{self.terminal.colors['RESET']}")
            
            print(f"\n{self.terminal.colors['CYAN']}Enjoy your day buddy!! by onex_dv{self.terminal.colors['RESET']}\n")
            
            return True
            
        except Exception as e:
            self.terminal.debug_error("SCAN", f"Scan failed: {str(e)}")
            return False
    
    def save_full_version(self, transactions, output_path):
        """Save full version data"""
        self.terminal.debug_step("SAVE", "Saving full version data")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("ALICE Bot - Full Transaction Data\n")
            f.write("="*80 + "\n\n")
            
            for tx in transactions:
                f.write(f"Hash: {tx['hash']}\n")
                f.write(f"Method: {tx['method']}\n")
                f.write(f"Age: {tx['age']}\n")
                f.write(f"From: {tx['from']}\n")
                f.write(f"To: {tx['to']}\n")
                f.write(f"Token: {tx['token']}\n")
                f.write("-" * 50 + "\n")
                
                # Debug output for full version
                self.terminal.debug_data("TX", f"Hash: {tx['hash'][:10]}... | From: {tx['from'][:10]}... | To: {tx['to'][:10]}... | Token: {tx['token']}")
    
    def save_from_version(self, transactions, output_path):
        """Save from version data (only wallet addresses)"""
        self.terminal.debug_step("SAVE", "Saving from version data")
        
        # Extract unique 'from' addresses
        from_addresses = list(set(tx['from'] for tx in transactions))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("ALICE Bot - Wallet Addresses (From)\n")
            f.write("="*80 + "\n\n")
            
            for address in from_addresses:
                f.write(f"{address}\n")
                
                # Debug output for from version
                self.terminal.debug_data("WALLET", f"From: {address}")

def main():
    """Main execution function"""
    bot = AliceBot()
    
    # Parse arguments
    if len(sys.argv) < 2:
        bot.show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command in ['h', 'help']:
        bot.show_help()
        return
    
    if command not in ['sc', 'scan']:
        print(f"Error: Unknown command '{command}'. Use 'help' for usage information.")
        return
    
    if len(sys.argv) != 6:
        print("Error: Invalid number of arguments.")
        bot.show_help()
        return
    
    wallet_address = sys.argv[2]
    action = sys.argv[3].lower()
    version = sys.argv[4]
    output_file = sys.argv[5]
    
    if action not in ['p', 'print']:
        print(f"Error: Invalid action '{action}'. Use 'p' or 'print'.")
        return
    
    if version.lower() not in ['vv', 'vf']:
        print(f"Error: Invalid version '{version}'. Use 'Vv' or 'Vf'.")
        return
    
    # Initialize bot
    if not bot.initialize():
        print("Failed to initialize bot. Check configuration and try again.")
        return
    
    # Show welcome screen
    bot.show_welcome()
    
    # Get user confirmation
    if not bot.confirm_scan():
        return
    
    # Execute scan
    bot.run_scan(wallet_address, version, output_file)

if __name__ == "__main__":
    main()
