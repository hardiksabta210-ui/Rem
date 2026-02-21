#!/usr/bin/env python3
"""
Build the launcher.py into a standalone .exe and place on Desktop
Run this script once to create the desktop launcher
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil

def build_exe():
    """Build launcher.py into an .exe file"""
    
    project_root = Path(__file__).parent.absolute()
    desktop = Path.home() / "Desktop"
    
    print("="*60)
    print("  BUILDING OPENCLAW + REM LAUNCHER EXE")
    print("="*60)
    
    # Check if PyInstaller is installed
    print("\n[*] Checking PyInstaller...")
    try:
        import PyInstaller
        print("[✓] PyInstaller is installed")
    except ImportError:
        print("[!] PyInstaller not found")
        print("[*] Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Build the .exe
    print(f"\n[*] Building executable from launcher.py...")
    print(f"    Output: {desktop}\\REM_Launcher.exe")
    
    launcher_py = project_root / "launcher.py"
    
    build_command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Single executable file
        "--console",  # Show console for debugging
        "--distpath", str(desktop),
        "--workpath", str(project_root / "build"),
        "--specpath", str(project_root / "build"),
        "--name", "REM_Launcher",
        str(launcher_py)
    ]
    
    try:
        result = subprocess.run(build_command, check=True)
        
        exe_path = desktop / "REM_Launcher.exe"
        if exe_path.exists():
            print(f"\n[✓] Successfully created: {exe_path}")
            
            # Create a batch file launcher as backup
            print("\n[*] Creating backup batch launcher...")
            bat_path = desktop / "Start_REM_Services.bat"
            with open(bat_path, 'w') as f:
                f.write(f'@echo off\ncd /d "{project_root}"\ncall .venv\\Scripts\\activate.bat\npython launcher.py\npause\n')
            print(f"[✓] Created: {bat_path}")
            
            print("\n" + "="*60)
            print("  ✓ BUILD COMPLETE")
            print("="*60)
            print(f"\nDesktop Launcher Created:")
            print(f"  • {exe_path}")
            print(f"  • {bat_path}")
            print("\nDouble-click 'REM_Launcher.exe' or 'Start_REM_Services.bat' to start all services!")
            
        else:
            print(f"\n[ERROR] Failed to create executable at {exe_path}")
            
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] PyInstaller build failed: {e}")
        print("\nTrying alternative: Creating batch file launcher only...")
        
        bat_path = desktop / "Start_REM_Services.bat"
        with open(bat_path, 'w') as f:
            f.write(f'@echo off\ncd /d "{project_root}"\ncall .venv\\Scripts\\activate.bat\npython launcher.py\npause\n')
        print(f"[✓] Created: {bat_path}")
        print("\nYou can use the batch file to start services.")
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")


if __name__ == "__main__":
    build_exe()
