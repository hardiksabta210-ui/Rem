@echo off
REM Clean restart - kills old processes and starts fresh

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo  CLEAN RESTART - KILLING OLD PROCESSES
echo ============================================================
echo.

REM Kill any existing Python processes on these ports
echo [*] Killing old processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr "8000 8765 5000"') do (
    taskkill /PID %%a /F >nul 2>&1
)

REM Extra kill for all python.exe to be safe
taskkill /F /IM python.exe >nul 2>&1

echo [✓] Old processes terminated
echo [*] Waiting for ports to free up...
timeout /t 2 /nobreak >nul

echo.
echo ============================================================
echo  STARTING FRESH SERVICES
echo ============================================================
echo.

set PROJECT_ROOT=%~dp0

REM Activate venv
if exist "%PROJECT_ROOT%.venv\Scripts\activate.bat" (
    call "%PROJECT_ROOT%.venv\Scripts\activate.bat"
)

REM 1. REM API Server
echo [1/3] Starting REM API Server...
start "REM API Server (Port 8000)" cmd /k "cd /d "%PROJECT_ROOT%" && python server\api_server_robust.py"
timeout /t 2 /nobreak >nul

REM 2. OpenClaw Bridge
echo [2/3] Starting OpenClaw Bridge...
start "OpenClaw Bridge (Port 8765)" cmd /k "cd /d "%PROJECT_ROOT%" && python server\bridge_server_robust.py"
timeout /t 2 /nobreak >nul

REM 3. Voice Chat
echo [3/3] Starting Voice Chat...
start "REM Voice Chat" cmd /k "cd /d "%PROJECT_ROOT%" && python server\main_chat.py"

echo.
echo ============================================================
echo  ✓ SERVICES RESTARTED
echo ============================================================
echo.
echo All services running on fresh ports:
echo   • API Server:     http://127.0.0.1:8000
echo   • Bridge:         http://127.0.0.1:8765
echo   • Voice Chat:     Ready for input
echo.
echo Press CTRL+C to stop services
echo ============================================================
echo.

pause
