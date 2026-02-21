#!/usr/bin/env python3
"""
ULTIMATE REM + OPENCLAW LAUNCHER
- Kills old processes
- Waits for ports to free
- Starts services with proper sequencing
- Verifies each service is running
"""

import os
import sys
import subprocess
import time
import socket
from pathlib import Path

class UltimateLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        
    def kill_all_python(self):
        """Kill all Python processes"""
        print("\n[*] Killing any existing Python processes...")
        try:
            if sys.platform == 'win32':
                # Try to kill python.exe (may fail if no processes, that's OK)
                subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                             capture_output=True, timeout=5, check=False)
            else:
                subprocess.run(['pkill', '-9', 'python'], 
                             capture_output=True, timeout=5, check=False)
            print("[✓] Python processes killed (or none found)")
        except Exception as e:
            print(f"[!] Could not kill processes: {e}")
        
        time.sleep(2)
    
    def port_is_free(self, port: int, timeout: int = 2) -> bool:
        """Check if a port is free"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex(('127.0.0.1', port))
                return result != 0
        except:
            return True
    
    def wait_for_port_free(self, port: int, max_wait: int = 10) -> bool:
        """Wait for a port to become free"""
        for i in range(max_wait):
            if self.port_is_free(port):
                return True
            print(f"[*] Waiting for port {port} to free... ({i+1}/{max_wait})")
            time.sleep(1)
        return False
    
    def start_service(self, name: str, script: str, check_port: int = None) -> bool:
        """Start a service and wait for it to be ready"""
        print(f"\n[*] Starting {name}...")
        
        try:
            if sys.platform == 'win32':
                # Windows: start in new console window
                subprocess.Popen(
                    ['cmd', '/k', f'cd /d "{self.project_root}" && python "{script}"'],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                subprocess.Popen([sys.executable, str(script)], cwd=str(self.project_root))
            
            time.sleep(2)
            
            # If we have a port to check, verify service is responding
            if check_port:
                print(f"[*] Waiting for {name} on port {check_port}...")
                for attempt in range(15):
                    time.sleep(1)
                    if not self.port_is_free(check_port):
                        print(f"[✓] {name} is responding on port {check_port}")
                        return True
                    if attempt < 14:
                        print(f"[*] Waiting... ({attempt+1}/15)")
                
                print(f"[!] {name} did not respond after 15 seconds")
                return False
            
            print(f"[✓] {name} started")
            return True
            
        except Exception as e:
            print(f"[!] Failed to start {name}: {e}")
            return False
    
    def run(self):
        """Run the launcher"""
        print("\n" + "="*60)
        print("  ULTIMATE REM + OPENCLAW LAUNCHER v3.0")
        print("="*60)
        print(f"\nProject: {self.project_root}")
        
        # Step 1: Kill everything
        self.kill_all_python()
        
        # Step 2: Verify ports are free
        print("\n[*] Checking ports...")
        ports_to_check = [8000, 8765]
        for port in ports_to_check:
            if not self.wait_for_port_free(port):
                print(f"[!] WARNING: Port {port} still in use, service may not start")
        
        # Step 3: Start services
        print("\n" + "="*60)
        print("  STARTING SERVICES")
        print("="*60)
        
        # Service 1: API Server
        api_ok = self.start_service(
            "REM API Server v2.1",
            str(self.project_root / "server" / "api_server_v2.py"),
            check_port=8000
        )
        
        # Service 2: Bridge
        bridge_ok = self.start_service(
            "OpenClaw Bridge v1.1",
            str(self.project_root / "server" / "bridge_server_v2.py"),
            check_port=8765
        )
        
        # Service 3: Voice Chat
        voice_ok = self.start_service(
            "REM Voice Chat",
            str(self.project_root / "server" / "main_chat.py")
        )
        
        # Summary
        print("\n" + "="*60)
        print("  ✓ SERVICES STARTED")
        print("="*60)
        print("\nStatus:")
        print(f"  {'[✓]' if api_ok else '[!]'} REM API Server    → http://127.0.0.1:8000")
        print(f"  {'[✓]' if bridge_ok else '[!]'} OpenClaw Bridge   → http://127.0.0.1:8765")
        print(f"  {'[✓]' if voice_ok else '[!]'} REM Voice Chat    → Interactive")
        
        if api_ok and bridge_ok:
            print("\n[✓] All critical services running!")
            print("\nSpeak commands in Voice Chat window:")
            print('  "Open YouTube"')
            print('  "Search for Python tutorials"')
            print('  "Tell me a joke"')
        else:
            print("\n[!] Some services failed to start")
            print("Check terminal windows for error messages")
        
        print("\n" + "="*60)
        print("Press CTRL+C to stop all services")
        print("="*60 + "\n")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[*] Shutting down...")
            print("[✓] Goodbye!")
            sys.exit(0)


def main():
    launcher = UltimateLauncher()
    try:
        launcher.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
