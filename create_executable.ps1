# PowerShell script to create a Windows executable from the batch file
# This uses IExpress (built into Windows) to create a self-extracting executable

param(
    [string]$OutputPath = "ZigbeePythonInstaller.exe"
)

Write-Host "Creating executable Python installer..." -ForegroundColor Cyan
Write-Host ""

# Create temporary SED file for IExpress
$sedContent = @"
[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=0
HideExtractAnimation=0
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
InstallPrompt=Do you want to install Python for the Zigbee Device Programmer?
DisplayLicense=
FinishMessage=Python installation process completed. You can now run the Zigbee Device Programmer.
TargetName=$PWD\$OutputPath
FriendlyName=Zigbee Device Programmer - Python Installer
AppLaunched=cmd.exe /c install_python_runner.bat
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
FILE0="install_python_runner.bat"
FILE1="install_python.bat"
FILE2="install_python.ps1"
FILE3="requirements.txt"

[SourceFiles]
SourceFiles0=$PWD\
[SourceFiles0]
%FILE0%=
%FILE1%=
%FILE2%=
%FILE3%=
"@

$sedFile = "python_installer.sed"
$sedContent | Out-File -FilePath $sedFile -Encoding ASCII

try {
    # Run IExpress to create the executable
    Write-Host "Running IExpress to create executable..." -ForegroundColor Yellow
    $process = Start-Process -FilePath "iexpress.exe" -ArgumentList "/N", $sedFile -Wait -PassThru -NoNewWindow
    
    if ($process.ExitCode -eq 0 -and (Test-Path $OutputPath)) {
        Write-Host ""
        Write-Host "✅ Successfully created: $OutputPath" -ForegroundColor Green
        Write-Host ""
        Write-Host "The executable installer includes:" -ForegroundColor White
        Write-Host "  - All installation scripts" -ForegroundColor Gray
        Write-Host "  - requirements.txt" -ForegroundColor Gray
        Write-Host "  - Automatic Python download and installation" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Users can now double-click $OutputPath to install Python automatically." -ForegroundColor Green
    } else {
        throw "IExpress failed to create executable"
    }
} catch {
    Write-Host ""
    Write-Host "❌ Failed to create executable: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative options:" -ForegroundColor Yellow
    Write-Host "1. Use install_python_runner.bat directly (already works as double-click)" -ForegroundColor Yellow
    Write-Host "2. Use a third-party tool like Bat2Exe or Advanced BAT to EXE Converter" -ForegroundColor Yellow
    Write-Host "3. Create an MSI installer using WiX Toolset" -ForegroundColor Yellow
} finally {
    # Clean up temporary files
    Remove-Item $sedFile -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Current installation options available:" -ForegroundColor Cyan
Write-Host "  - install_python_runner.bat (double-click ready)" -ForegroundColor White
if (Test-Path $OutputPath) {
    Write-Host "  - $OutputPath (executable installer)" -ForegroundColor White
}
Write-Host ""