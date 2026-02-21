@echo off
REM Create a Windows shortcut for the launcher on the Desktop
REM This uses VBScript to create a proper .lnk shortcut

setlocal enabledelayedexpansion
set PROJECT_ROOT=%~dp0

echo.
echo ============================================================
echo  CREATING DESKTOP SHORTCUT
echo ============================================================
echo.

REM Create VBScript to make shortcut
set VBSCRIPT=%TEMP%\create_shortcut.vbs

(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = oWS.SpecialFolders("Desktop"^) ^& "\REM_Launcher.lnk"
    echo sTargetPath = "%PROJECT_ROOT%launcher.py"
    echo sWorkingDir = "%PROJECT_ROOT%"
    echo sIconPath = "%PROJECT_ROOT%.venv\Lib\site-packages\openclaw\icon.ico"
    echo.
    echo Set oLink = oWS.CreateLink(sLinkFile^)
    echo oLink.TargetPath = "python"
    echo oLink.Arguments = sTargetPath
    echo oLink.WorkingDirectory = sWorkingDir
    echo oLink.Description = "REM + OpenClaw Launcher"
    echo if Fso.FileExists(sIconPath^) Then
    echo   oLink.IconLocation = sIconPath
    echo End If
    echo oLink.Save
) > "%VBSCRIPT%"

REM Run the VBScript
cscript //b "%VBSCRIPT%"

REM Check if shortcut was created
if exist "%USERPROFILE%\Desktop\REM_Launcher.lnk" (
    echo.
    echo [✓] Desktop shortcut created successfully!
    echo [✓] Location: %USERPROFILE%\Desktop\REM_Launcher.lnk
    echo.
    echo You can now double-click the REM_Launcher shortcut to start all services.
) else (
    echo.
    echo [!] Shortcut creation may have failed
    echo [*] You can manually create a shortcut:
    echo    1. Right-click on launcher.py
    echo    2. Send to ^> Desktop (create shortcut^)
)

REM Clean up
del /q "%VBSCRIPT%" >nul 2>&1

echo.
pause
