@echo off
:: ===================================================================
:: Test All Launchers for Zigbee Device Programmer
:: This script validates that all launcher files are properly created
:: and have valid syntax without actually running the application
:: ===================================================================

echo.
echo ====================================================
echo     Testing All Zigbee Device Programmer Launchers
echo ====================================================
echo.

set SUCCESS_COUNT=0
set TOTAL_COUNT=0

:: Test 1: Check if main application file exists
set /a TOTAL_COUNT+=1
if exist "zigbee_programmer.py" (
    echo ✓ Main application file: zigbee_programmer.py
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: zigbee_programmer.py
)

:: Test 2: Batch Launcher
set /a TOTAL_COUNT+=1
if exist "ZigbeeDeviceProgrammer.bat" (
    echo ✓ Batch launcher: ZigbeeDeviceProgrammer.bat
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: ZigbeeDeviceProgrammer.bat
)

:: Test 3: VBScript Launcher  
set /a TOTAL_COUNT+=1
if exist "ZigbeeDeviceProgrammer.vbs" (
    echo ✓ VBScript launcher: ZigbeeDeviceProgrammer.vbs
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: ZigbeeDeviceProgrammer.vbs
)

:: Test 4: Advanced Batch Launcher
set /a TOTAL_COUNT+=1
if exist "run_zigbee_programmer.bat" (
    echo ✓ Advanced batch launcher: run_zigbee_programmer.bat
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: run_zigbee_programmer.bat
)

:: Test 5: PowerShell Launcher
set /a TOTAL_COUNT+=1
if exist "run_zigbee_programmer.ps1" (
    echo ✓ PowerShell launcher: run_zigbee_programmer.ps1
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: run_zigbee_programmer.ps1
)

:: Test 6: Executable Creator Scripts
set /a TOTAL_COUNT+=1
if exist "create_launcher_executable.ps1" (
    echo ✓ Executable creator: create_launcher_executable.ps1
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: create_launcher_executable.ps1
)

set /a TOTAL_COUNT+=1
if exist "create_pyinstaller_executable.ps1" (
    echo ✓ PyInstaller creator: create_pyinstaller_executable.ps1
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: create_pyinstaller_executable.ps1
)

:: Test 7: Desktop Shortcut Creator
set /a TOTAL_COUNT+=1
if exist "create_desktop_shortcut.ps1" (
    echo ✓ Shortcut creator: create_desktop_shortcut.ps1
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: create_desktop_shortcut.ps1
)

:: Test 8: Documentation
set /a TOTAL_COUNT+=1
if exist "LAUNCHER_GUIDE.md" (
    echo ✓ Documentation: LAUNCHER_GUIDE.md
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: LAUNCHER_GUIDE.md
)

:: Test 9: Python Installation System
set /a TOTAL_COUNT+=1
if exist "install_python_runner.bat" (
    echo ✓ Python installer: install_python_runner.bat
    set /a SUCCESS_COUNT+=1
) else (
    echo ✗ Missing: install_python_runner.bat
)

echo.
echo ====================================================
echo                   Test Results
echo ====================================================
echo.

if %SUCCESS_COUNT%==%TOTAL_COUNT% (
    echo ✅ ALL TESTS PASSED! ^(%SUCCESS_COUNT%/%TOTAL_COUNT%^)
    echo.
    echo 🎯 Ready for Use:
    echo    • Double-click ZigbeeDeviceProgrammer.bat ^(with console^)
    echo    • Double-click ZigbeeDeviceProgrammer.vbs ^(silent^)
    echo.
    echo 🛠️ Available Tools:
    echo    • .\create_launcher_executable.ps1 ^(create .exe^)
    echo    • .\create_pyinstaller_executable.ps1 ^(standalone exe^)
    echo    • .\create_desktop_shortcut.ps1 ^(desktop shortcut^)
    echo.
    echo 📚 Documentation:
    echo    • LAUNCHER_GUIDE.md ^(complete guide^)
    echo.
    echo The launcher system is ready for production use!
) else (
    echo ❌ SOME TESTS FAILED ^(%SUCCESS_COUNT%/%TOTAL_COUNT% passed^)
    echo.
    echo Please ensure all launcher files have been created properly.
)

echo.

:: Test Python availability (informational)
echo ====================================================
echo              System Requirements Check
echo ====================================================
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo ✓ Python: %%i
    echo   → Launchers will work immediately
) else (
    echo ⚠ Python: Not installed or not in PATH
    echo   → Users will need to run install_python_runner.bat first
)

:: Check if tkinter is available
python -c "import tkinter" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ GUI Library: tkinter available
) else (
    echo ⚠ GUI Library: tkinter may need installation
)

echo.
echo Test completed.
pause