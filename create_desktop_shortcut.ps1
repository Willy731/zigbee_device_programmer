# ===================================================================
# Create Desktop Shortcut for Zigbee Device Programmer
# This creates a shortcut on the desktop for easy access
# ===================================================================

param(
    [string]$LauncherType = "batch"  # Options: batch, vbs, exe
)

Write-Host "Creating desktop shortcut for Zigbee Device Programmer..." -ForegroundColor Cyan
Write-Host ""

# Get current directory
$currentDir = Get-Location

# Determine launcher file based on type
switch ($LauncherType.ToLower()) {
    "batch" { 
        $launcherFile = "ZigbeeDeviceProgrammer.bat"
        $description = "Zigbee Device Programmer (Batch Launcher)"
    }
    "vbs" { 
        $launcherFile = "ZigbeeDeviceProgrammer.vbs"
        $description = "Zigbee Device Programmer (Silent Launcher)"
    }
    "exe" { 
        $launcherFile = "ZigbeeDeviceProgrammer.exe"
        $description = "Zigbee Device Programmer (Executable)"
    }
    default {
        Write-Host "Invalid launcher type. Use: batch, vbs, or exe" -ForegroundColor Red
        exit 1
    }
}

$launcherPath = Join-Path $currentDir $launcherFile

# Check if launcher file exists
if (-not (Test-Path $launcherPath)) {
    Write-Host "ERROR: Launcher file not found: $launcherFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available launchers to create shortcut for:" -ForegroundColor Yellow
    
    $availableLaunchers = @()
    if (Test-Path "ZigbeeDeviceProgrammer.bat") { $availableLaunchers += "batch (ZigbeeDeviceProgrammer.bat)" }
    if (Test-Path "ZigbeeDeviceProgrammer.vbs") { $availableLaunchers += "vbs (ZigbeeDeviceProgrammer.vbs)" }
    if (Test-Path "ZigbeeDeviceProgrammer.exe") { $availableLaunchers += "exe (ZigbeeDeviceProgrammer.exe)" }
    
    if ($availableLaunchers.Count -gt 0) {
        foreach ($launcher in $availableLaunchers) {
            Write-Host "  • $launcher" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "Example: .\create_desktop_shortcut.ps1 -LauncherType batch" -ForegroundColor Cyan
    } else {
        Write-Host "  None found. Please create a launcher first." -ForegroundColor Red
    }
    
    exit 1
}

# Get desktop path
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "Zigbee Device Programmer.lnk"

try {
    # Create WScript Shell COM object
    $WshShell = New-Object -ComObject WScript.Shell
    
    # Create shortcut
    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $launcherPath
    $shortcut.WorkingDirectory = $currentDir
    $shortcut.Description = $description
    $shortcut.WindowStyle = 1  # Normal window
    
    # Set icon if available (try to use Python icon or default)
    $iconPath = ""
    
    # Try to find Python icon
    try {
        $pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
        if ($pythonPath) {
            $pythonDir = Split-Path $pythonPath -Parent
            $possibleIcons = @(
                (Join-Path $pythonDir "python.exe"),
                (Join-Path $pythonDir "..\DLLs\py.ico"),
                (Join-Path $pythonDir "..\python.exe")
            )
            
            foreach ($icon in $possibleIcons) {
                if (Test-Path $icon) {
                    $iconPath = $icon
                    break
                }
            }
        }
    } catch {
        # Ignore errors finding Python icon
    }
    
    if ($iconPath) {
        $shortcut.IconLocation = $iconPath
        Write-Host "Using Python icon: $iconPath" -ForegroundColor Gray
    } else {
        # Use default system icon for batch/executable files
        Write-Host "Using default system icon" -ForegroundColor Gray
    }
    
    # Save the shortcut
    $shortcut.Save()
    
    Write-Host ""
    Write-Host "✅ Desktop shortcut created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Shortcut Details:" -ForegroundColor Cyan
    Write-Host "  📁 Location: $shortcutPath" -ForegroundColor White
    Write-Host "  🎯 Target: $launcherFile" -ForegroundColor White
    Write-Host "  📝 Description: $description" -ForegroundColor White
    Write-Host "  📂 Working Directory: $currentDir" -ForegroundColor White
    Write-Host ""
    Write-Host "The shortcut is now available on your desktop!" -ForegroundColor Green
    Write-Host "Double-click it to launch the Zigbee Device Programmer." -ForegroundColor Green
    
} catch {
    Write-Host ""
    Write-Host "❌ Failed to create desktop shortcut: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Manual shortcut creation:" -ForegroundColor Yellow
    Write-Host "  1. Right-click on desktop → New → Shortcut" -ForegroundColor White
    Write-Host "  2. Target: $launcherPath" -ForegroundColor White
    Write-Host "  3. Name: Zigbee Device Programmer" -ForegroundColor White
    
} finally {
    # Clean up COM object
    if ($WshShell) {
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($WshShell) | Out-Null
    }
}

Write-Host ""