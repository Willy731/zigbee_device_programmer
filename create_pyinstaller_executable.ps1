# ===================================================================
# Create Standalone Executable using PyInstaller
# This creates a true executable that includes Python runtime
# ===================================================================

param(
    [switch]$OneFile = $true,
    [switch]$Windowed = $true,
    [switch]$Console = $false
)

Write-Host "Creating standalone executable with PyInstaller..." -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
try {
    $pyinstallerVersion = python -m PyInstaller --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller not found"
    }
    Write-Host "✓ PyInstaller found: $pyinstallerVersion" -ForegroundColor Green
} catch {
    Write-Host "PyInstaller not installed. Installing..." -ForegroundColor Yellow
    python -m pip install pyinstaller
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install PyInstaller" -ForegroundColor Red
        Write-Host ""
        Write-Host "Manual installation:" -ForegroundColor Yellow
        Write-Host "  pip install pyinstaller" -ForegroundColor White
        exit 1
    }
    Write-Host "✓ PyInstaller installed successfully" -ForegroundColor Green
}

# Check if main Python file exists
if (-not (Test-Path "zigbee_programmer.py")) {
    Write-Host "❌ zigbee_programmer.py not found!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Building executable..." -ForegroundColor Yellow

# Build PyInstaller command
$pyinstallerArgs = @()

if ($OneFile) {
    $pyinstallerArgs += "--onefile"
    Write-Host "  • Single file executable" -ForegroundColor Gray
}

if ($Windowed -and -not $Console) {
    $pyinstallerArgs += "--windowed"
    Write-Host "  • No console window (GUI only)" -ForegroundColor Gray
} else {
    Write-Host "  • Console window enabled" -ForegroundColor Gray
}

# Add icon if available
$iconPath = ""
$possibleIcons = @(
    "icon.ico",
    "app.ico", 
    "zigbee.ico",
    "programmer.ico"
)

foreach ($icon in $possibleIcons) {
    if (Test-Path $icon) {
        $iconPath = $icon
        break
    }
}

if ($iconPath) {
    $pyinstallerArgs += "--icon=$iconPath"
    Write-Host "  • Using icon: $iconPath" -ForegroundColor Gray
}

# Add additional options
$pyinstallerArgs += @(
    "--name=ZigbeeDeviceProgrammer",
    "--clean",
    "--noconfirm"
)

# Add hidden imports for common issues
$pyinstallerArgs += "--hidden-import=tkinter"
$pyinstallerArgs += "--hidden-import=tkinter.ttk"
$pyinstallerArgs += "--hidden-import=tkinter.filedialog"
$pyinstallerArgs += "--hidden-import=tkinter.messagebox"

# Add data files if they exist
$dataFiles = @(
    "device_mapping.json",
    "custom_device_mapping.json",
    "zigbee_programmer_settings.json"
)

foreach ($file in $dataFiles) {
    if (Test-Path $file) {
        $pyinstallerArgs += "--add-data=$file;."
        Write-Host "  • Including data file: $file" -ForegroundColor Gray
    }
}

$pyinstallerArgs += "zigbee_programmer.py"

Write-Host ""
Write-Host "Running: python -m PyInstaller $($pyinstallerArgs -join ' ')" -ForegroundColor Gray
Write-Host ""

try {
    # Run PyInstaller
    $process = Start-Process -FilePath "python" -ArgumentList (@("-m", "PyInstaller") + $pyinstallerArgs) -Wait -PassThru -NoNewWindow
    
    if ($process.ExitCode -eq 0) {
        # Check for created executable
        $exePath = ""
        if ($OneFile) {
            $exePath = "dist\ZigbeeDeviceProgrammer.exe"
        } else {
            $exePath = "dist\ZigbeeDeviceProgrammer\ZigbeeDeviceProgrammer.exe"
        }
        
        if (Test-Path $exePath) {
            Write-Host ""
            Write-Host "✅ Executable created successfully!" -ForegroundColor Green
            
            $fileInfo = Get-Item $exePath
            $fileSizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
            
            Write-Host ""
            Write-Host "Executable Details:" -ForegroundColor Cyan
            Write-Host "  📄 File: $exePath" -ForegroundColor White
            Write-Host "  📏 Size: $fileSizeMB MB" -ForegroundColor White
            Write-Host "  🐍 Python Runtime: Included" -ForegroundColor White
            Write-Host "  📦 Dependencies: Bundled" -ForegroundColor White
            Write-Host ""
            Write-Host "Benefits:" -ForegroundColor Green
            Write-Host "  ✓ No Python installation required on target system" -ForegroundColor White
            Write-Host "  ✓ No dependency issues" -ForegroundColor White
            Write-Host "  ✓ Single file distribution" -ForegroundColor White
            Write-Host "  ✓ Professional deployment option" -ForegroundColor White
            Write-Host ""
            
            # Ask if user wants to create desktop shortcut
            $createShortcut = Read-Host "Create desktop shortcut? (Y/N)"
            if ($createShortcut -match "^[Yy]") {
                try {
                    $desktopPath = [Environment]::GetFolderPath("Desktop")
                    $shortcutPath = Join-Path $desktopPath "Zigbee Device Programmer.lnk"
                    
                    $WshShell = New-Object -ComObject WScript.Shell
                    $shortcut = $WshShell.CreateShortcut($shortcutPath)
                    $shortcut.TargetPath = (Resolve-Path $exePath).Path
                    $shortcut.WorkingDirectory = (Get-Location).Path
                    $shortcut.Description = "Zigbee Device Programmer (Standalone)"
                    $shortcut.Save()
                    
                    Write-Host "✓ Desktop shortcut created: $shortcutPath" -ForegroundColor Green
                } catch {
                    Write-Host "⚠ Failed to create desktop shortcut: $($_.Exception.Message)" -ForegroundColor Yellow
                }
            }
            
        } else {
            Write-Host "⚠ Executable not found at expected location: $exePath" -ForegroundColor Yellow
            Write-Host "Check the dist/ folder for the created executable." -ForegroundColor Yellow
        }
        
    } else {
        throw "PyInstaller failed with exit code: $($process.ExitCode)"
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Failed to create executable: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  • Check that all imports work: python zigbee_programmer.py" -ForegroundColor White
    Write-Host "  • Try without --windowed flag for debug info" -ForegroundColor White
    Write-Host "  • Check PyInstaller logs in build/ folder" -ForegroundColor White
    Write-Host ""
    Write-Host "Alternative launchers:" -ForegroundColor Cyan
    Write-Host "  • ZigbeeDeviceProgrammer.bat (batch launcher)" -ForegroundColor White
    Write-Host "  • ZigbeeDeviceProgrammer.vbs (silent launcher)" -ForegroundColor White
}

Write-Host ""