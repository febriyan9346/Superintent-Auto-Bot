import os
import time
import random
from datetime import datetime
import pytz
from colorama import Fore, Style, init
import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_checksum_address
from datetime import datetime, timezone
import json
from typing import Optional, Dict
import warnings

os.system('clear' if os.name == 'posix' else 'cls')

warnings.filterwarnings('ignore')

import sys
if not sys.warnoptions:
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)


class SuperintentBot:
    def __init__(self):
        self.wib = pytz.timezone('Asia/Jakarta')
    
    def get_wib_time(self):
        return datetime.now(self.wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}SUPERINTENT.AI AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)
    
    def read_file(self, filename):
        try:
            with open(filename, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
        except Exception:
            return []
    
    def create_session(self, private_key, proxy=None, cf_clearance=None):
        if not private_key.startswith('0x'):
            private_key = '0x' + private_key
        
        account = Account.from_key(private_key)
        address = to_checksum_address(account.address)
        
        proxies = None
        if proxy:
            proxies = {
                'http': proxy,
                'https': proxy
            }
        
        base_url = "https://bff-root.superintent.ai"
        origin = "https://mission.superintent.ai"
        
        session = requests.Session()
        session.headers.update({
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': origin,
            'referer': f'{origin}/',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        })
        
        if cf_clearance:
            session.cookies.set('cf_clearance', cf_clearance, domain='.superintent.ai')
        
        return {
            'session': session,
            'address': address,
            'account': account,
            'proxies': proxies,
            'base_url': base_url,
            'origin': origin
        }
    
    def get_nonce(self, ctx):
        try:
            url = f"{ctx['base_url']}/v1/auth/nonce"
            response = ctx['session'].get(url, proxies=ctx['proxies'], timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('nonce')
        except Exception:
            return None
    
    def sign_message(self, ctx, nonce):
        try:
            issued_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            
            message = (
                f"mission.superintent.ai wants you to sign in with your Ethereum account:\n"
                f"{ctx['address']}\n\n"
                f"To securely sign in, please sign this message to verify you're the owner of this wallet.\n\n"
                f"URI: https://mission.superintent.ai\n"
                f"Version: 1\n"
                f"Chain ID: 1\n"
                f"Nonce: {nonce}\n"
                f"Issued At: {issued_at}"
            )
            
            message_hash = encode_defunct(text=message)
            signed_message = ctx['account'].sign_message(message_hash)
            signature = '0x' + signed_message.signature.hex() if not signed_message.signature.hex().startswith('0x') else signed_message.signature.hex()
            
            return message, signature
        except Exception:
            return None, None
    
    def login(self, ctx):
        try:
            nonce = self.get_nonce(ctx)
            if not nonce:
                return False
            
            message, signature = self.sign_message(ctx, nonce)
            if not message or not signature:
                return False
            
            url = f"{ctx['base_url']}/v1/auth/siwe"
            payload = {
                "message": message,
                "signature": signature
            }
            
            response = ctx['session'].post(url, json=payload, proxies=ctx['proxies'], timeout=30)
            response.raise_for_status()
            return True
        except Exception:
            return False
    
    def check_in(self, ctx):
        try:
            url = f"{ctx['base_url']}/v1/check-in"
            response = ctx['session'].post(url, proxies=ctx['proxies'], timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
    
    def get_stats(self, ctx):
        try:
            url = f"{ctx['base_url']}/v1/me/stats"
            response = ctx['session'].get(url, proxies=ctx['proxies'], timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
    
    def get_checkin_status(self, ctx):
        try:
            url = f"{ctx['base_url']}/v1/check-in/status"
            response = ctx['session'].get(url, proxies=ctx['proxies'], timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
    
    def process_account(self, private_key, proxy, cf_clearance, account_num, total_accounts):
        try:
            ctx = self.create_session(private_key, proxy, cf_clearance)
            
            self.log(f"Account #{account_num}/{total_accounts}", "INFO")
            
            if proxy:
                proxy_display = proxy.split('@')[1] if '@' in proxy else proxy
                self.log(f"Proxy: {proxy_display}", "INFO")
            else:
                self.log(f"Proxy: No Proxy", "INFO")
            
            self.log(f"Address: {ctx['address'][:6]}...{ctx['address'][-4:]}", "INFO")
            
            time.sleep(random.randint(1, 3))
            
            if not self.login(ctx):
                self.log("Login failed!", "ERROR")
                return False
            
            self.log("Login successful!", "SUCCESS")
            
            time.sleep(random.randint(1, 2))
            
            checkin_status = self.get_checkin_status(ctx)
            if checkin_status:
                has_checked_in = checkin_status.get('hasCheckedInToday', False)
                current_streak = checkin_status.get('currentStreak', 0)
                
                if not has_checked_in:
                    checkin_result = self.check_in(ctx)
                    if checkin_result and checkin_result.get('success'):
                        points_granted = checkin_result.get('pointsGranted', 0)
                        self.log(f"Check-in Success! Reward: +{points_granted} Points | Streak: {current_streak}", "SUCCESS")
                    else:
                        self.log("Check-in failed!", "ERROR")
                else:
                    self.log(f"Already checked in today | Streak: {current_streak}", "WARNING")
            
            time.sleep(random.randint(1, 2))
            
            stats = self.get_stats(ctx)
            if stats:
                total_points = stats.get('totalPoints', 0)
                referral_count = stats.get('referralCount', 0)
                self.log(f"Total Points: {total_points} | Referrals: {referral_count}", "INFO")
            
            return True
            
        except Exception as e:
            self.log(f"Error: {str(e)}", "ERROR")
            return False
    
    def run(self):
        self.print_banner()
        
        choice = self.show_menu()
        use_proxy = (choice == '1')
        
        accounts = self.read_file('accounts.txt')
        proxies = self.read_file('proxy.txt') if use_proxy else []
        
        cf_clearance = None
        try:
            cf_cookies = self.read_file('cf_clearance.txt')
            if cf_cookies:
                cf_clearance = cf_cookies[0]
                self.log("Cloudflare clearance loaded", "INFO")
        except:
            pass
        
        if not accounts:
            self.log("No accounts found in accounts.txt", "ERROR")
            return
        
        if use_proxy:
            self.log(f"Running with proxy", "INFO")
        else:
            self.log(f"Running without proxy", "INFO")
        
        self.log(f"Loaded {len(accounts)} accounts successfully", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            total_accounts = len(accounts)
            
            for idx, private_key in enumerate(accounts, 1):
                proxy = None
                if proxies:
                    proxy = proxies[(idx - 1) % len(proxies)]
                
                if self.process_account(private_key, proxy, cf_clearance, idx, total_accounts):
                    success_count += 1
                
                if idx < total_accounts:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{total_accounts}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            
            wait_time = 86400
            self.countdown(wait_time)


if __name__ == "__main__":
    bot = SuperintentBot()
    bot.run()
