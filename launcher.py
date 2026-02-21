#!/usr/bin/env python3
"""
REM + OPENCLAW LAUNCHER - Production Version
- Clean, simple, reliable
- Uses proven robust servers with dynamic port allocation
"""

import subprocess
import sys
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class Launcher:
    def __init__(self):
        self.project = Path(__file__).parent.absolute()
        self.server_dir = self.project / "server"
    
    def check_port(self, port: int, timeout: int = 2) -> bool:
        """Check if a port is accepting connections"""
        try:
            response = requests.get(f'http://127.0.0.1:{port}/health', timeout=timeout)
            return response.status_code in [200, 404]
        except:
            return False
    
    def start(self):
        """Start all services"""
        logger.info("\n" + "="*70)
        logger.info(" REM + OPENCLAW SYSTEM LAUNCHER")
        logger.info("="*70)
        
        # Start services
        self.start_api_server()
        time.sleep(2)
        self.start_bridge()
        time.sleep(2)
        self.start_voice_chat()
        
        # Summary
        logger.info("\n" + "="*70)
        logger.info(" SERVICES RUNNING")
        logger.info("="*70)
        logger.info("\nYour REM + OpenClaw system is ready!")
        logger.info("\nSpeak commands in the voice chat window:")
        logger.info('  • "Open YouTube"')
        logger.info('  • "Search for python tutorials"')
        logger.info('  • "Tell me a joke"')
        logger.info("\nPress Ctrl+C to stop all services\n")
        logger.info("="*70 + "\n")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n\nShutting down...")
            sys.exit(0)
    
    def start_api_server(self):
        """Start REM API server"""
        logger.info("\n[1] Starting REM API Server...")
        try:
            if sys.platform == 'win32':
                subprocess.Popen(
                    f'start "" cmd /k "cd {self.server_dir} && python api_server_robust.py"',
                    shell=True
                )
            else:
                subprocess.Popen(
                    ["python3", str(self.server_dir / "api_server_robust.py")],
                    cwd=str(self.server_dir)
                )
            logger.info("    ✓ API Server started")
        except Exception as e:
            logger.error(f"    ✗ Failed: {e}")
    
    def start_bridge(self):
        """Start OpenClaw Bridge"""
        logger.info("[2] Starting OpenClaw Bridge...")
        try:
            if sys.platform == 'win32':
                subprocess.Popen(
                    f'start "" cmd /k "cd {self.server_dir} && python bridge_server_robust.py"',
                    shell=True
                )
            else:
                subprocess.Popen(
                    ["python3", str(self.server_dir / "bridge_server_robust.py")],
                    cwd=str(self.server_dir)
                )
            logger.info("    ✓ Bridge started")
        except Exception as e:
            logger.error(f"    ✗ Failed: {e}")
    
    def start_voice_chat(self):
        """Start voice chat interface"""
        logger.info("[3] Starting Voice Chat...")
        try:
            if sys.platform == 'win32':
                subprocess.Popen(
                    f'start "" cmd /k "cd {self.project} && python server/main_chat.py"',
                    shell=True
                )
            else:
                subprocess.Popen(
                    ["python3", str(self.project / "server" / "main_chat.py")],
                    cwd=str(self.project)
                )
            logger.info("    ✓ Voice Chat started")
        except Exception as e:
            logger.error(f"    ✗ Failed: {e}")


def main():
    try:
        launcher = Launcher()
        launcher.start()
    except Exception as e:
        logger.error(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
