# ===================================================================
# Python Installation Script for Zigbee Device Programmer
# PowerShell version - More robust error handling and features
# ===================================================================

param(
    [switch]$Silent = $false
)

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    if (-not $Silent) {
        Write-Host $Message -ForegroundColor $Color
    }
}

# Function to check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Main installation function
function Install-Python {
    Write-ColorOutput ""
    Write-ColorOutput "====================================================" "Cyan"
    Write-ColorOutput "   Python Installation for Zigbee Device Programmer" "Cyan"
    Write-ColorOutput "====================================================" "Cyan"
    Write-ColorOutput ""

    # Check if Python is already installed
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "Python is already installed!" "Green"
            Write-ColorOutput "Version: $pythonVersion" "Green"
            Write-ColorOutput ""
            Install-Packages
            return
        }
    } catch {
        # Python not found, continue with installation
    }

    Write-ColorOutput "Python is not installed. Starting installation process..." "Yellow"
    Write-ColorOutput ""

    # Python version configuration
    $pythonVersion = "3.12.0"
    $pythonInstaller = "python-$pythonVersion-amd64.exe"
    $downloadUrl = "https://www.python.org/ftp/python/$pythonVersion/$pythonInstaller"
    $tempDir = "$env:TEMP\zigbee_python_install"
    $installerPath = "$tempDir\$pythonInstaller"

    # Create temp directory
    if (-not (Test-Path $tempDir)) {
        New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    }

    Write-ColorOutput "Downloading Python $pythonVersion..." "Yellow"
    Write-ColorOutput "From: $downloadUrl" "Gray"
    Write-ColorOutput ""

    # Download Python installer
    try {
        Write-ColorOutput "Downloading installer... (This may take a few minutes)" "Yellow"
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing

        if (-not (Test-Path $installerPath)) {
            throw "Download failed - file not found"
        }

        Write-ColorOutput "Download completed successfully!" "Green"
        Write-ColorOutput ""
    } catch {
        Write-ColorOutput "ERROR: Failed to download Python installer!" "Red"
        Write-ColorOutput "Error: $($_.Exception.Message)" "Red"
        Write-ColorOutput "Please check your internet connection and try again." "Red"
        Write-ColorOutput ""
        if (-not $Silent) { Read-Host "Press Enter to continue..." }
        exit 1
    }

    # Install Python
    Write-ColorOutput "Installing Python... (This will take a few minutes)" "Yellow"
    Write-ColorOutput "Please wait while Python is being installed..." "Yellow"

    $installArgs = @(
        "/quiet"
        "InstallAllUsers=0"
        "PrependPath=1" 
        "Include_test=0"
        "Include_pip=1"
        "Include_tcltk=1"
    )

    try {
        $process = Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -PassThru
        
        if ($process.ExitCode -ne 0) {
            throw "Installation failed with exit code: $($process.ExitCode)"
        }

        # Wait for installation to complete and refresh environment
        Start-Sleep -Seconds 5
        
        # Refresh PATH environment variable
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")

        # Verify installation
        $pythonCheck = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python installation verification failed"
        }

        Write-ColorOutput ""
        Write-ColorOutput "Python installation completed successfully!" "Green"
        Write-ColorOutput "Version: $pythonCheck" "Green"
        Write-ColorOutput ""

        # Clean up installer
        Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

    } catch {
        Write-ColorOutput ""
        Write-ColorOutput "ERROR: Python installation failed!" "Red"
        Write-ColorOutput "Error: $($_.Exception.Message)" "Red"
        Write-ColorOutput ""
        Write-ColorOutput "Troubleshooting tips:" "Yellow"
        Write-ColorOutput "1. Try running this script as Administrator" "Yellow"
        Write-ColorOutput "2. Temporarily disable antivirus software" "Yellow"
        Write-ColorOutput "3. Install Python manually from: https://www.python.org/downloads/" "Yellow"
        Write-ColorOutput ""
        if (-not $Silent) { Read-Host "Press Enter to continue..." }
        exit 1
    }

    Install-Packages
}

# Function to install required packages
function Install-Packages {
    Write-ColorOutput "Installing required Python packages..." "Yellow"
    Write-ColorOutput ""

    # Get script directory
    $scriptDir = Split-Path -Parent $MyInvocation.ScriptName
    if (-not $scriptDir) {
        $scriptDir = Get-Location
    }

    $requirementsPath = Join-Path $scriptDir "requirements.txt"

    # Check if requirements.txt exists
    if (-not (Test-Path $requirementsPath)) {
        Write-ColorOutput "WARNING: requirements.txt not found!" "Yellow"
        Write-ColorOutput "Creating basic requirements.txt with essential packages..." "Yellow"
        
        $basicRequirements = @(
            "# Basic requirements for Zigbee Device Programmer"
            "pytest>=7.0.0"
            "# tkinter is included with Python installation"
        )
        $basicRequirements | Out-File -FilePath $requirementsPath -Encoding UTF8
    }

    # Install packages
    try {
        Write-ColorOutput "Installing packages from requirements.txt..." "Yellow"
        
        # Upgrade pip first
        python -m pip install --upgrade pip
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "WARNING: Failed to upgrade pip" "Yellow"
        }

        # Install requirements
        python -m pip install -r $requirementsPath
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "WARNING: Some packages may have failed to install." "Yellow"
            Write-ColorOutput "You can try running manually: python -m pip install -r requirements.txt" "Yellow"
        } else {
            Write-ColorOutput "All packages installed successfully!" "Green"
        }

    } catch {
        Write-ColorOutput "WARNING: Package installation encountered errors." "Yellow"
        Write-ColorOutput "Error: $($_.Exception.Message)" "Yellow"
        Write-ColorOutput "You may need to install packages manually." "Yellow"
    }

    Write-ColorOutput ""
    Write-ColorOutput "====================================================" "Cyan"
    Write-ColorOutput "   Installation Complete!" "Cyan"
    Write-ColorOutput "====================================================" "Cyan"
    Write-ColorOutput ""
    Write-ColorOutput "Python and required packages have been installed." "Green"
    Write-ColorOutput "You can now run the Zigbee Device Programmer by:" "White"
    Write-ColorOutput "  1. Double-clicking zigbee_programmer.py, or" "White"
    Write-ColorOutput "  2. Running: python zigbee_programmer.py" "White"
    Write-ColorOutput ""
    Write-ColorOutput "If you encounter any issues, please check:" "Yellow"
    Write-ColorOutput "  - Python is in your system PATH" "Yellow"
    Write-ColorOutput "  - All required packages are installed" "Yellow"
    Write-ColorOutput "  - You have proper permissions" "Yellow"
    Write-ColorOutput ""

    if (-not $Silent) {
        Read-Host "Press Enter to continue..."
    }
}

# Main execution
try {
    # Set execution policy for this session if needed
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

    Install-Python
} catch {
    Write-ColorOutput "FATAL ERROR: $($_.Exception.Message)" "Red"
    if (-not $Silent) {
        Read-Host "Press Enter to exit..."
    }
    exit 1
}