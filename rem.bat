@echo off
REM REM Command Launcher for Windows
REM Unified interface for REM + OpenClaw services

setlocal enabledelayedexpansion

REM Get the directory of this script
set SCRIPT_DIR=%~dp0

REM Run Python script with all arguments
python "%SCRIPT_DIR%rem" %*

exit /b %errorlevel%
