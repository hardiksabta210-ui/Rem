@echo off
REM ============================================================
REM OpenClaw + REM Services Launcher - FIXED
REM Robust version that won't crash
REM ============================================================

setlocal enabledelayedexpansion

set PROJECT_ROOT=%~dp0
set VENV_ACTIVATE=%PROJECT_ROOT%.venv\Scripts\activate.bat

echo.
echo ============================================================
echo  OPENCLAW + REM SERVICES LAUNCHER
echo ============================================================
echo.

REM Activate virtual environment
if exist "%VENV_ACTIVATE%" (
    call "%VENV_ACTIVATE%"
    echo [✓] Virtual environment activated
) else (
    echo [!] Virtual environment not found at %VENV_ACTIVATE%
)

echo.
echo ============================================================
echo  STARTING SERVICES
echo ============================================================
echo.

REM Service 1: REM API Server
echo [1/3] Starting REM API Server...
start "REM API Server" cmd /k "cd /d "%PROJECT_ROOT%" && python server\api_server_robust.py"
timeout /t 3 /nobreak > nul

REM Service 2: OpenClaw Bridge
echo [2/3] Starting OpenClaw Bridge...
start "OpenClaw Bridge" cmd /k "cd /d "%PROJECT_ROOT%" && python server\bridge_server_robust.py"
timeout /t 3 /nobreak > nul

REM Service 3: Voice Chat
echo [3/3] Starting REM Voice Chat...
start "REM Voice Chat" cmd /k "cd /d "%PROJECT_ROOT%" && python server\main_chat.py"

echo.
echo ============================================================
echo  ✓ ALL SERVICES STARTED
echo ============================================================
echo.
echo Services Running:
echo   • REM API Server       → http://127.0.0.1:8000
echo   • OpenClaw Bridge      → http://127.0.0.1:8765
echo   • REM Voice Chat       → Ready for voice input
echo.
echo [✓] Ready to use! Speak commands in REM Voice Chat window.
echo.
echo ============================================================
echo Press CTRL+C in any window to close it
echo ============================================================
echo.

pause
