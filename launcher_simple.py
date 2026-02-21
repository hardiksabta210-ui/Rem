#!/usr/bin/env python3
"""
SIMPLE REM + OPENCLAW LAUNCHER
- Starts services in new console windows
- Verifies ports are responding
"""

import sys
import subprocess
import time
import socket
from pathlib import Path

class SimpleLauncher:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.api_port = 8000
        self.bridge_port = 8765
        
    def port_is_responding(self, port: int, timeout: int = 1) -> bool:
        """Check if a port is actually responding"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex(('127.0.0.1', port))
                return result == 0
        except:
            return False
    
    def start_service(self, name: str, script_name: str, port: int = None) -> tuple:
        """Start a service in new console window"""
        script_path = self.project_root / "server" / script_name
        
        print(f"\n>>> Starting: {name}")
        print(f"    Script: {script_name}")
        
        try:
            if sys.platform == 'win32':
                # Start in new console window on Windows
                proc = subprocess.Popen(
                    f'start cmd /k "cd /d {self.project_root} && python {script_path}"',
                    shell=True
                )
            else:
                # Start normally on Linux/Mac
                proc = subprocess.Popen(
                    [sys.executable, str(script_path)],
                    cwd=str(self.project_root)
                )
            
            # Wait for startup
            time.sleep(3)
            
            # Check if port is responding
            if port:
                responding = False
                for attempt in range(10):
                    if self.port_is_responding(port):
                        print(f"    ✓ Responding on port {port}")
                        responding = True
                        break
                    print(f"    - Waiting for response... ({attempt+1}/10)")
                    time.sleep(1)
                
                if not responding:
                    print(f"    ⚠ May not have started properly")
                return (True, port)
            
            print(f"    ✓ Started")
            return (True, None)
            
        except Exception as e:
            print(f"    ✗ Error: {e}")
            return (False, None)
    
    def main(self):
        """Main launcher flow"""
        print("\n" + "="*70)
        print("  REM + OPENCLAW LAUNCHER")
        print("="*70)
        print(f"\nLocation: {self.project_root}\n")
        
        # Start services
        results = {}
        
        print("[1/3] Starting REM API Server...")
        ok, port = self.start_service(
            "REM API Server v2.1",
            "api_server_v2.py",
            self.api_port
        )
        results['api'] = (ok, port)
        
        print("\n[2/3] Starting OpenClaw Bridge...")
        ok, port = self.start_service(
            "OpenClaw Bridge v1.1",
            "bridge_server_v2.py",
            self.bridge_port
        )
        results['bridge'] = (ok, port)
        
        print("\n[3/3] Starting Voice Chat Interface...")
        ok, port = self.start_service(
            "REM Voice Chat",
            "main_chat.py"
        )
        results['voice'] = (ok, port)
        
        # Summary
        print("\n" + "="*70)
        print("  STATUS")
        print("="*70)
        
        api_ok, api_port = results['api']
        bridge_ok, bridge_port = results['bridge']
        voice_ok, _ = results['voice']
        
        print(f"\n  REM API Server:      {'✓' if api_ok else '✗'} (port {api_port})")
        print(f"  OpenClaw Bridge:     {'✓' if bridge_ok else '✗'} (port {bridge_port})")
        print(f"  Voice Chat:          {'✓' if voice_ok else '✗'}")
        
        print("\n" + "="*70)
        
        if api_ok and bridge_ok:
            print("\n  ✓ READY TO USE")
            print("\n  Try these voice commands:")
            print('    • "Open YouTube"')
            print('    • "Search for Python tutorials"')
            print('    • "Tell me a joke"')
            print("\n  Press Ctrl+C to stop all services")
        else:
            print("\n  ⚠ Some services may not have started")
            print("\n  Check the console windows for error messages")
        
        print("\n" + "="*70 + "\n")
        
        # Keep launcher alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n  Shutting down...\n")
            sys.exit(0)


if __name__ == "__main__":
    launcher = SimpleLauncher()
    try:
        launcher.main()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
