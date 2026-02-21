@echo off
REM ============================================================
REM OpenClaw + REM Services Launcher
REM This batch file starts all required services in order
REM ============================================================

setlocal enabledelayedexpansion

REM Get project root directory
set PROJECT_ROOT=%~dp0

echo.
echo ============================================================
echo  OPENCLAW + REM SERVICES LAUNCHER
echo ============================================================
echo.
echo Project Root: %PROJECT_ROOT%
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo [*] Activating Python virtual environment...
    call "%PROJECT_ROOT%.venv\Scripts\activate.bat"
    if errorlevel 1 (
        echo [ERROR] Failed to activate virtual environment
        pause
        exit /b 1
    )
)

echo [✓] Python virtual environment activated
echo.

REM Check if Ollama is running
echo [*] Checking Ollama service...
timeout /t 1 /nobreak > nul
powershell -Command "try { $null = Invoke-WebRequest -Uri 'http://127.0.0.1:11434/api/tags' -ErrorAction Stop; Write-Host '[✓] Ollama is running'; exit 0 } catch { Write-Host '[!] Ollama is NOT running - please start: ollama serve'; exit 1 }"
if errorlevel 1 (
    echo.
    echo [!] WARNING: Ollama service not detected
    echo [!] Please start Ollama in a separate terminal: ollama serve
    echo.
    pause
)

echo.
echo ============================================================
echo  Starting Services...
echo ============================================================
echo.

REM Terminal 1: REM API Server
echo [1/4] Starting REM API Server on port 8000...
start "REM API Server" cmd /k "cd /d "%PROJECT_ROOT%" && python server/api_v2.py"
timeout /t 3 /nobreak > nul

REM Terminal 2: OpenClaw Bridge
echo [2/4] Starting OpenClaw Bridge on port 8765...
start "OpenClaw Bridge" cmd /k "cd /d "%PROJECT_ROOT%" && python server/openclaw_bridge.py"
timeout /t 3 /nobreak > nul

REM Terminal 3: OpenClaw Gateway
echo [3/4] Starting OpenClaw Gateway...
start "OpenClaw Gateway" cmd /k "cd /d "%PROJECT_ROOT%\openclaw" && openclaw gateway"
timeout /t 3 /nobreak > nul

REM Terminal 4: REM Voice Chat
echo [4/4] Starting REM Voice Chat Interface...
start "REM Voice Chat" cmd /k "cd /d "%PROJECT_ROOT%" && python server/main_chat.py"

echo.
echo ============================================================
echo  ✓ All Services Started Successfully!
echo ============================================================
echo.
echo Services Running:
echo   1. REM API Server       → http://127.0.0.1:8000
echo   2. OpenClaw Bridge      → http://127.0.0.1:8765
echo   3. OpenClaw Gateway     → ws://127.0.0.1:9001
echo   4. REM Voice Chat       → Interactive Terminal
echo.
echo Ready to use! Speak voice commands in the "REM Voice Chat" window.
echo.
echo To stop all services:
echo   1. Close each terminal window
echo   2. Or press CTRL+C in any window
echo.
echo ============================================================
echo.

REM Keep this window open
pause
