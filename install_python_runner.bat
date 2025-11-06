@echo off
:: Simple wrapper to run the PowerShell installation script
:: This handles PowerShell execution policy issues

echo Starting Python Installation for Zigbee Device Programmer...
echo.

:: Try to run PowerShell script first (more robust)
powershell.exe -ExecutionPolicy Bypass -File "%~dp0install_python.ps1"

if %errorlevel% neq 0 (
    echo.
    echo PowerShell script failed, falling back to batch script...
    echo.
    call "%~dp0install_python.bat"
)

echo.
echo Installation process completed.
pause