# ===================================================================
# Create Executable Launcher for Zigbee Device Programmer
# This creates a Windows .exe file that can be double-clicked
# ===================================================================

param(
    [string]$OutputName = "ZigbeeDeviceProgrammer.exe",
    [switch]$IncludeFiles = $false
)

Write-Host "Creating executable launcher for Zigbee Device Programmer..." -ForegroundColor Cyan
Write-Host ""

# Verify required files exist
$requiredFiles = @(
    "zigbee_programmer.py",
    "run_zigbee_programmer.bat"
)

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "ERROR: Required file not found: $file" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ All required files found" -ForegroundColor Green

# Create IExpress SED file for the executable
$sedContent = @"
[Version]
Class=IEXPRESS
SEDVersion=3

[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=1
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName=%TargetName%
FriendlyName=%FriendlyName%
AppLaunched=%AppLaunched%
PostInstallCmd=%PostInstallCmd%
AdminQuietInstCmd=%AdminQuietInstCmd%
UserQuietInstCmd=%UserQuietInstCmd%
SourceFiles=SourceFiles

[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetName=$PWD\$OutputName
FriendlyName=Zigbee Device Programmer
AppLaunched=cmd.exe /c run_zigbee_programmer.bat
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
FILE0="run_zigbee_programmer.bat"
FILE1="zigbee_programmer.py"
"@

# Add additional files if requested
if ($IncludeFiles) {
    Write-Host "Including additional support files..." -ForegroundColor Yellow
    
    $additionalFiles = @(
        "requirements.txt",
        "device_mapping.json",
        "commander_manager.py",
        "device_manager.py",
        "file_operations.py",
        "ui_theme.py",
        "version_parser.py"
    )
    
    $fileIndex = 2
    foreach ($file in $additionalFiles) {
        if (Test-Path $file) {
            $sedContent += "`nFILE$fileIndex=`"$file`""
            $fileIndex++
            Write-Host "  + Including: $file" -ForegroundColor Gray
        }
    }
}

$sedContent += @"

[SourceFiles]
SourceFiles0=$PWD\
[SourceFiles0]
%FILE0%=
%FILE1%=
"@

# Add source file references for additional files
if ($IncludeFiles) {
    for ($i = 2; $i -lt $fileIndex; $i++) {
        $sedContent += "`n%FILE$i%="
    }
}

# Write SED file
$sedFile = "zigbee_launcher.sed"
$sedContent | Out-File -FilePath $sedFile -Encoding ASCII

try {
    Write-Host ""
    Write-Host "Creating executable with IExpress..." -ForegroundColor Yellow
    
    # Run IExpress to create the executable
    $process = Start-Process -FilePath "iexpress.exe" -ArgumentList "/N", $sedFile -Wait -PassThru -NoNewWindow
    
    if ($process.ExitCode -eq 0 -and (Test-Path $OutputName)) {
        Write-Host ""
        Write-Host "✅ Successfully created: $OutputName" -ForegroundColor Green
        
        # Get file size
        $fileInfo = Get-Item $OutputName
        $fileSizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
        
        Write-Host ""
        Write-Host "Executable Details:" -ForegroundColor Cyan
        Write-Host "  📄 File: $OutputName" -ForegroundColor White
        Write-Host "  📏 Size: $fileSizeMB MB" -ForegroundColor White
        Write-Host "  🗂️ Contains: Python launcher and core files" -ForegroundColor White
        Write-Host ""
        Write-Host "Usage Instructions:" -ForegroundColor Cyan
        Write-Host "  • Double-click $OutputName to run the application" -ForegroundColor White
        Write-Host "  • Create desktop shortcut for easy access" -ForegroundColor White
        Write-Host "  • Distribute as single executable file" -ForegroundColor White
        Write-Host ""
        Write-Host "Requirements:" -ForegroundColor Yellow
        Write-Host "  • Python must be installed on target system" -ForegroundColor White
        Write-Host "  • Use install_python_runner.bat if Python not available" -ForegroundColor White
        
    } else {
        throw "IExpress failed to create executable (Exit code: $($process.ExitCode))"
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Failed to create executable: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative solutions:" -ForegroundColor Yellow
    Write-Host "  1. Use ZigbeeDeviceProgrammer.bat (batch launcher)" -ForegroundColor White
    Write-Host "  2. Use ZigbeeDeviceProgrammer.vbs (silent launcher)" -ForegroundColor White
    Write-Host "  3. Install PyInstaller: pip install pyinstaller" -ForegroundColor White
    Write-Host "     Then run: pyinstaller --onefile --windowed zigbee_programmer.py" -ForegroundColor White
    
} finally {
    # Clean up temporary files
    Remove-Item $sedFile -ErrorAction SilentlyContinue
}

Write-Host ""