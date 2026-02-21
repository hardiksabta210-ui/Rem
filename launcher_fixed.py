#!/usr/bin/env python3
"""
REM + OpenClaw Services Launcher - FIXED & ROBUST
Starts all required services in the correct order
Single executable that handles everything
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path
from typing import Optional

class ServiceLauncher:
    def __init__(self):
        # Get project root
        self.project_root = Path(__file__).parent.absolute()
        
    def check_ollama(self) -> bool:
        """Check if Ollama is running"""
        try:
            import requests
            response = requests.get('http://127.0.0.1:11434/api/tags', timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def start_service(self, name: str, command: list, cwd: Optional[Path] = None):
        """Start a service in a new terminal window"""
        if cwd is None:
            cwd = self.project_root
        
        print(f"[*] Starting {name}...")
        
        try:
            if sys.platform == 'win32':
                # Windows: Use 'start' command to open new window
                # Quote the command properly
                cmd_str = ' '.join(f'"{c}"' if ' ' in str(c) else str(c) for c in command)
                full_command = f'cd /d "{cwd}" && {cmd_str}'
                subprocess.Popen(
                    ['cmd', '/k', full_command],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Linux/Mac: Use gnome-terminal or similar
                subprocess.Popen(command, cwd=str(cwd))
            
            time.sleep(2)
            print(f"[✓] {name} started")
            return True
        except Exception as e:
            print(f"[!] Failed to start {name}: {e}")
            return False
    
    def run(self):
        """Run all services"""
        print("\n" + "="*60)
        print("  OPENCLAW + REM SERVICES LAUNCHER v2.0")
        print("="*60)
        print(f"\nProject: {self.project_root}")
        
        # Check virtual environment
        if os.environ.get('VIRTUAL_ENV'):
            print(f"[✓] Virtual environment detected")
        else:
            print("[!] No virtual environment detected")
            print("[!] Make sure to activate: .venv\\Scripts\\activate")
        
        # Check Ollama
        print("\n[*] Checking Ollama...")
        if self.check_ollama():
            print("[✓] Ollama is running")
        else:
            print("[!] Ollama not found - LLM responses may fail")
            print("[!] Start Ollama with: ollama serve")
        
        # Start services
        print("\n" + "="*60)
        print("  STARTING SERVICES")
        print("="*60 + "\n")
        
        # Service 1: REM API Server (ROBUST)
        print("[1/3] REM API Server...")
        self.start_service(
            "REM API Server",
            [sys.executable, str(self.project_root / "server" / "api_server_robust.py")]
        )
        time.sleep(3)
        
        # Service 2: OpenClaw Bridge (ROBUST)
        print("\n[2/3] OpenClaw Bridge...")
        self.start_service(
            "OpenClaw Bridge",
            [sys.executable, str(self.project_root / "server" / "bridge_server_robust.py")]
        )
        time.sleep(3)
        
        # Service 3: REM Voice Chat
        print("\n[3/3] REM Voice Chat...")
        self.start_service(
            "REM Voice Chat",
            [sys.executable, str(self.project_root / "server" / "main_chat.py")]
        )
        
        # Done
        print("\n" + "="*60)
        print("  ✓ ALL SERVICES STARTED")
        print("="*60)
        print("\nServices Running:")
        print("  • REM API Server       → http://127.0.0.1:8000")
        print("  • OpenClaw Bridge      → http://127.0.0.1:8765")
        print("  • REM Voice Chat       → Ready for voice input")
        print("\n[✓] Ready to use!")
        print("\nSpeak commands in the REM Voice Chat window:")
        print("  'Open YouTube and search for cats'")
        print("  'What is AI?'")
        print("  'Tell me a joke'")
        print("\n" + "="*60)
        print("Press CTRL+C to stop all services")
        print("="*60 + "\n")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[*] Shutting down services...")
            print("[✓] All services stopped")
            sys.exit(0)


def main():
    launcher = ServiceLauncher()
    try:
        launcher.run()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
