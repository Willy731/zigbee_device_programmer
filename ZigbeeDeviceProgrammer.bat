@echo off
:: ===================================================================
:: Universal Zigbee Device Programmer Launcher
:: Tries PowerShell first, falls back to batch if needed
:: This ensures compatibility across all Windows systems
:: ===================================================================

setlocal

:: Set window title
title Zigbee Device Programmer

echo.
echo ====================================================
echo     Zigbee Device Programmer - Universal Launcher
echo ====================================================
echo.

:: Change to script directory
cd /d "%~dp0"

:: Try PowerShell launcher first (better user experience)
echo Attempting to start with enhanced PowerShell launcher...
powershell.exe -ExecutionPolicy Bypass -File "%~dp0run_zigbee_programmer.ps1" -NoWait 2>nul

:: Check if PowerShell succeeded
if %errorlevel% equ 0 (
    echo PowerShell launcher completed successfully.
    goto :end
)

:: If PowerShell failed, fall back to batch launcher
echo.
echo PowerShell launcher unavailable, using batch launcher...
echo.
call "%~dp0run_zigbee_programmer.bat"

:end
echo.
echo Launcher finished.
:: Brief pause so user can see any final messages
timeout /t 2 /nobreak >nul 2>&1
exit /b %errorlevel%