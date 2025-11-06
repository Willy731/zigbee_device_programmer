@echo off
setlocal enabledelayedexpansion

:: ===================================================================
:: Python Installation Script for Zigbee Device Programmer
:: This script will automatically download and install Python if needed
:: ===================================================================

echo.
echo ====================================================
echo   Python Installation for Zigbee Device Programmer
echo ====================================================
echo.

:: Check if Python is already installed
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python is already installed!
    python --version
    echo.
    goto :install_packages
)

echo Python is not installed. Starting installation process...
echo.

:: Set Python version to install (latest stable)
set PYTHON_VERSION=3.12.0
set PYTHON_INSTALLER=python-!PYTHON_VERSION!-amd64.exe
set DOWNLOAD_URL=https://www.python.org/ftp/python/!PYTHON_VERSION!/!PYTHON_INSTALLER!

echo Downloading Python !PYTHON_VERSION!...
echo From: !DOWNLOAD_URL!
echo.

:: Create temp directory if it doesn't exist
if not exist "%TEMP%\zigbee_python_install" mkdir "%TEMP%\zigbee_python_install"
cd /d "%TEMP%\zigbee_python_install"

:: Download Python installer using PowerShell
echo Downloading installer... (This may take a few minutes)
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%PYTHON_INSTALLER%'}"

if not exist "!PYTHON_INSTALLER!" (
    echo.
    echo ERROR: Failed to download Python installer!
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo Download completed successfully!
echo.

:: Install Python with options:
:: - /quiet: Silent installation
:: - InstallAllUsers=0: Install for current user only
:: - PrependPath=1: Add Python to PATH
:: - Include_test=0: Don't include test suite
:: - Include_pip=1: Include pip package manager
echo Installing Python... (This will take a few minutes)
echo Please wait while Python is being installed...

"!PYTHON_INSTALLER!" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_pip=1

:: Wait a moment for installation to complete
timeout /t 5 /nobreak >nul

:: Refresh environment variables
call :refresh_env

:: Verify Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python installation failed or Python is not in PATH!
    echo Please try running this script as Administrator or install Python manually.
    echo Visit: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo Python installation completed successfully!
python --version
echo.

:: Clean up installer
del "!PYTHON_INSTALLER!" >nul 2>&1

:install_packages
:: Navigate back to the project directory
cd /d "%~dp0"

echo Installing required Python packages...
echo.

:: Check if requirements.txt exists
if not exist "requirements.txt" (
    echo WARNING: requirements.txt not found!
    echo Creating basic requirements.txt with essential packages...
    echo tkinter>requirements.txt
    echo pytest>>requirements.txt
)

:: Install packages from requirements.txt
echo Installing packages from requirements.txt...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo WARNING: Some packages may have failed to install.
    echo You can try running: python -m pip install -r requirements.txt
    echo.
) else (
    echo.
    echo All packages installed successfully!
)

echo.
echo ====================================================
echo   Installation Complete!
echo ====================================================
echo.
echo Python and required packages have been installed.
echo You can now run the Zigbee Device Programmer by:
echo   1. Double-clicking zigbee_programmer.py, or
echo   2. Running: python zigbee_programmer.py
echo.
echo If you encounter any issues, please check:
echo   - Python is in your system PATH
echo   - All required packages are installed
echo   - You have proper permissions
echo.

pause
goto :eof

:: Function to refresh environment variables
:refresh_env
:: This attempts to refresh the PATH without requiring a restart
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "UserPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SystemPath=%%b"
set "PATH=%SystemPath%;%UserPath%"
goto :eof