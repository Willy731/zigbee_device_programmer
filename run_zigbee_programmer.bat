@echo off
:: ===================================================================
:: Zigbee Device Programmer Launcher
:: Double-click this file to run the Zigbee Device Programmer
:: ===================================================================

:: Set window title
title Zigbee Device Programmer

:: Change to the directory where this script is located
cd /d "%~dp0"

echo.
echo ====================================================
echo        Starting Zigbee Device Programmer
echo ====================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo To install Python automatically, double-click:
    echo   install_python_runner.bat
    echo.
    echo Or install Python manually from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Display Python version
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Using: %PYTHON_VERSION%
echo.

:: Check if zigbee_programmer.py exists
if not exist "zigbee_programmer.py" (
    echo ERROR: zigbee_programmer.py not found!
    echo Please make sure you're running this from the correct directory.
    echo Expected location: %~dp0zigbee_programmer.py
    echo.
    pause
    exit /b 1
)

:: Check if required packages are installed
echo Checking required packages...
python -c "import tkinter; print('O GUI library (tkinter) available')" 2>nul
if %errorlevel% neq 0 (
    echo WARNING: GUI library (tkinter) not available!
    echo Installing required packages...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install required packages!
        echo Please run: python -m pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo ✓ All requirements satisfied
echo.
echo Starting Zigbee Device Programmer...
echo.

:: Run the application
python zigbee_programmer.py

:: Check exit status
if %errorlevel% neq 0 (
    echo.
    echo ====================================================
    echo   Application exited with error code: %errorlevel%
    echo ====================================================
    echo.
    echo If you encounter issues:
    echo 1. Check that Simplicity Commander is installed and in PATH
    echo 2. Ensure device permissions are properly configured
    echo 3. Try running as Administrator if needed
    echo.
    echo For detailed troubleshooting, see:
    echo   - PERMISSION_GUIDE.md
    echo   - README.md
    echo.
) else (
    echo.
    echo Application closed successfully.
)

:: Keep window open briefly so user can see any messages
timeout /t 3 /nobreak >nul 2>&1
exit /b %errorlevel%