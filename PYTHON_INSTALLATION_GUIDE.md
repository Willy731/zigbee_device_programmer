# Python Installation for Zigbee Device Programmer

This directory contains automated Python installation scripts for users who don't have Python installed on their system.

## Quick Start

**For most users**: Simply double-click `install_python_runner.bat`

This will automatically:
1. Check if Python is already installed
2. Download and install Python if needed
3. Install all required packages
4. Set up the environment for running the Zigbee Device Programmer

## Installation Files

### Main Installation Scripts

- **`install_python_runner.bat`** - **RECOMMENDED** - Main entry point that handles both PowerShell and batch execution
- **`install_python.ps1`** - Advanced PowerShell script with better error handling and colored output
- **`install_python.bat`** - Fallback batch script compatible with older Windows systems

### How to Use

1. **Double-click `install_python_runner.bat`**
   - This is the easiest method and handles all compatibility issues
   - Will automatically choose the best installation method for your system

2. **Alternative: Run PowerShell script directly**
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File install_python.ps1
   ```

3. **Alternative: Run batch script directly**
   ```cmd
   install_python.bat
   ```

## What Gets Installed

### Python Installation
- **Version**: Python 3.12.0 (latest stable)
- **Location**: User profile (no admin rights required)
- **Components**: 
  - Python interpreter
  - pip package manager
  - tkinter (GUI library)
  - Standard library

### Package Installation
- All packages listed in `requirements.txt`
- Automatic pip upgrade
- Essential packages for the Zigbee Device Programmer

## System Requirements

- **Operating System**: Windows 7 or later
- **Architecture**: 64-bit (the scripts download the 64-bit version)
- **Internet Connection**: Required for downloading Python and packages
- **Disk Space**: ~100MB for Python installation
- **Permissions**: No administrator rights required (installs for current user)

## Troubleshooting

### Common Issues

#### 1. PowerShell Execution Policy Error
**Error**: "execution of scripts is disabled on this system"
**Solution**: Use `install_python_runner.bat` which handles this automatically

#### 2. Download Failed
**Error**: "Failed to download Python installer"
**Solutions**:
- Check internet connection
- Try running as Administrator
- Temporarily disable antivirus/firewall
- Manual download from [python.org](https://www.python.org/downloads/)

#### 3. Installation Failed
**Error**: "Python installation failed"
**Solutions**:
- Run as Administrator
- Ensure sufficient disk space
- Close other applications during installation
- Try manual installation from [python.org](https://www.python.org/downloads/)

#### 4. Python Not Found After Installation
**Error**: "Python is not recognized as an internal or external command"
**Solutions**:
- Restart command prompt/terminal
- Log out and log back in
- Manually add Python to PATH
- Reinstall with "Add to PATH" option

### Manual Installation Steps

If the automated scripts fail, you can install manually:

1. **Download Python**:
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.12.0 or later
   - Choose "Windows installer (64-bit)"

2. **Install Python**:
   - Run the installer
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
   - Click "Install Now"

3. **Install Packages**:
   ```cmd
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. **Verify Installation**:
   ```cmd
   python --version
   python -c "import tkinter; print('GUI library available')"
   ```

## Security Notes

- The scripts download Python from the official python.org website
- All downloads use HTTPS (TLS 1.2)
- No sensitive data is collected or transmitted
- Installation is performed for the current user only (no system-wide changes)

## Advanced Usage

### Silent Installation
For automated deployments, you can run the PowerShell script silently:
```powershell
powershell.exe -ExecutionPolicy Bypass -File install_python.ps1 -Silent
```

### Custom Python Version
To install a different Python version, edit the `$pythonVersion` variable in `install_python.ps1` or the `PYTHON_VERSION` variable in `install_python.bat`.

### Behind Corporate Firewall
If you're behind a corporate firewall:
1. Download Python installer manually to the same directory
2. Rename it to match the expected filename (e.g., `python-3.12.0-amd64.exe`)
3. Run the installation script

## Support

If you encounter issues not covered in this guide:
1. Check the [Python installation documentation](https://docs.python.org/3/using/windows.html)
2. Verify system requirements
3. Try manual installation steps
4. Contact your system administrator for permission issues

## Files Created

After successful installation, you should have:
- Python installed in your user profile
- All required packages installed
- Environment variables configured
- Ability to run `python zigbee_programmer.py`

The installation scripts will create temporary files in your system's temp directory, which are automatically cleaned up after installation.