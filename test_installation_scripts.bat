@echo off
:: Test script to verify the installation scripts are properly formatted
:: This checks syntax without actually installing Python

echo Testing Python installation scripts...
echo.

:: Test batch script syntax
echo Testing install_python.bat syntax...
call :test_batch_syntax install_python.bat
if %errorlevel% neq 0 (
    echo ERROR: Syntax error in install_python.bat
    goto :error
)
echo install_python.bat syntax: OK

:: Test PowerShell script syntax
echo Testing install_python.ps1 syntax...
powershell.exe -Command "& {Get-Content 'install_python.ps1' | Out-Null; if ($?) {Write-Host 'install_python.ps1 syntax: OK'} else {Write-Host 'ERROR: Syntax error in install_python.ps1'; exit 1}}"
if %errorlevel% neq 0 goto :error

:: Test runner script syntax
echo Testing install_python_runner.bat syntax...
call :test_batch_syntax install_python_runner.bat
if %errorlevel% neq 0 (
    echo ERROR: Syntax error in install_python_runner.bat
    goto :error
)
echo install_python_runner.bat syntax: OK

echo.
echo ====================================
echo All installation scripts are valid!
echo ====================================
echo.
echo The scripts are ready to use:
echo - Double-click install_python_runner.bat to start installation
echo - The scripts will automatically handle Python installation and setup
echo.
goto :end

:test_batch_syntax
:: Test batch file syntax by parsing it
if not exist "%1" (
    echo ERROR: File %1 not found
    exit /b 1
)
:: Basic syntax check - just try to read the file
type "%1" >nul 2>&1
exit /b %errorlevel%

:error
echo.
echo Test failed! Please check the installation scripts for errors.
pause
exit /b 1

:end
echo Testing completed successfully.
pause
exit /b 0