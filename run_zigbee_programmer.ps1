# ===================================================================
# Zigbee Device Programmer Launcher (PowerShell)
# Advanced launcher with better error handling and user experience
# ===================================================================

param(
    [switch]$NoWait = $false,
    [switch]$Debug = $false
)

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Function to check Python installation
function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✓ Python found: $pythonVersion" "Green"
            return $true
        }
    } catch {
        # Python not found
    }
    
    Write-ColorOutput "✗ Python is not installed or not in PATH!" "Red"
    Write-ColorOutput ""
    Write-ColorOutput "To install Python automatically:" "Yellow"
    Write-ColorOutput "  → Double-click: install_python_runner.bat" "Cyan"
    Write-ColorOutput ""
    Write-ColorOutput "Or install manually:" "Yellow"
    Write-ColorOutput "  → Visit: https://www.python.org/downloads/" "Cyan"
    Write-ColorOutput "  → Make sure to check 'Add Python to PATH'" "Cyan"
    return $false
}

# Function to check required packages
function Test-RequiredPackages {
    Write-ColorOutput "Checking required packages..." "Yellow"
    
    try {
        # Check tkinter (GUI library)
        python -c "import tkinter; print('✓ GUI library available')" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "Installing GUI library..." "Yellow"
            python -m pip install -r requirements.txt
            if ($LASTEXITCODE -ne 0) {
                throw "Failed to install required packages"
            }
        }
        
        Write-ColorOutput "✓ All required packages available" "Green"
        return $true
    } catch {
        Write-ColorOutput "✗ Package installation failed: $($_.Exception.Message)" "Red"
        Write-ColorOutput "Try running: python -m pip install -r requirements.txt" "Yellow"
        return $false
    }
}

# Function to run the application
function Start-ZigbeeProgram {
    try {
        Write-ColorOutput ""
        Write-ColorOutput "🚀 Starting Zigbee Device Programmer..." "Cyan"
        Write-ColorOutput ""
        
        if ($Debug) {
            Write-ColorOutput "Debug mode enabled - showing detailed output" "Yellow"
            python zigbee_programmer.py
        } else {
            # Run normally
            python zigbee_programmer.py
        }
        
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0) {
            Write-ColorOutput ""
            Write-ColorOutput "✓ Application closed successfully" "Green"
        } else {
            Write-ColorOutput ""
            Write-ColorOutput "⚠ Application exited with code: $exitCode" "Yellow"
            Write-ColorOutput ""
            Write-ColorOutput "Troubleshooting tips:" "Cyan"
            Write-ColorOutput "• Check that Simplicity Commander is installed" "White"
            Write-ColorOutput "• Verify device connections and permissions" "White"
            Write-ColorOutput "• Try running as Administrator if needed" "White"
            Write-ColorOutput "• See PERMISSION_GUIDE.md for detailed help" "White"
        }
        
        return $exitCode
    } catch {
        Write-ColorOutput ""
        Write-ColorOutput "✗ Failed to start application: $($_.Exception.Message)" "Red"
        return 1
    }
}

# Main execution
function Main {
    # Set console title
    $Host.UI.RawUI.WindowTitle = "Zigbee Device Programmer Launcher"
    
    # Clear screen and show header
    Clear-Host
    Write-ColorOutput ""
    Write-ColorOutput "====================================================" "Cyan"
    Write-ColorOutput "        Zigbee Device Programmer Launcher" "Cyan"
    Write-ColorOutput "====================================================" "Cyan"
    Write-ColorOutput ""
    
    # Change to script directory
    $scriptDir = Split-Path -Parent $MyInvocation.ScriptName
    if ($scriptDir) {
        Set-Location $scriptDir
        Write-ColorOutput "Working directory: $scriptDir" "Gray"
    }
    Write-ColorOutput ""
    
    # Check if zigbee_programmer.py exists
    if (-not (Test-Path "zigbee_programmer.py")) {
        Write-ColorOutput "✗ zigbee_programmer.py not found!" "Red"
        Write-ColorOutput "Please ensure you're running this from the correct directory." "Yellow"
        Write-ColorOutput "Expected: $(Join-Path (Get-Location) 'zigbee_programmer.py')" "Gray"
        Write-ColorOutput ""
        if (-not $NoWait) { Read-Host "Press Enter to continue..." }
        return 1
    }
    
    # Check Python installation
    if (-not (Test-PythonInstallation)) {
        Write-ColorOutput ""
        if (-not $NoWait) { Read-Host "Press Enter to continue..." }
        return 1
    }
    
    # Check required packages
    if (-not (Test-RequiredPackages)) {
        Write-ColorOutput ""
        if (-not $NoWait) { Read-Host "Press Enter to continue..." }
        return 1
    }
    
    # Run the application
    $exitCode = Start-ZigbeeProgram
    
    # Wait for user input unless NoWait is specified
    if (-not $NoWait -and $exitCode -ne 0) {
        Write-ColorOutput ""
        Read-Host "Press Enter to continue..."
    }
    
    return $exitCode
}

# Run main function
try {
    # Set execution policy for this session
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force -ErrorAction SilentlyContinue
    
    $result = Main
    exit $result
} catch {
    Write-ColorOutput "FATAL ERROR: $($_.Exception.Message)" "Red"
    if (-not $NoWait) {
        Read-Host "Press Enter to exit..."
    }
    exit 1
}