# Zigbee Device Programmer - Permission and Access Issues

## Overview
This document describes the enhancements made to the Zigbee Device Programmer to handle Simplicity Commander access and permission issues.

## Problem
The original error occurred because:
1. Simplicity Commander (`commander`) was not found in the system PATH
2. The application lacked proper error handling for missing dependencies
3. No guidance was provided for permission issues

## Solution Implemented

### 1. Automatic Commander Detection
The application now automatically searches for Simplicity Commander in common installation locations:

**Windows:**
- `C:\SiliconLabs\SimplicityStudio\v5\developer\adapter_packs\commander\Commander.exe`
- `C:\SiliconLabs\SimplicityStudio\v4\developer\adapter_packs\commander\Commander.exe`
- `C:\Program Files\Silicon Labs\Simplicity Studio\v5\developer\adapter_packs\commander\Commander.exe`
- `C:\Program Files\Silicon Labs\Simplicity Studio\v4\developer\adapter_packs\commander\Commander.exe`
- `C:\Program Files (x86)\Silicon Labs\Simplicity Studio\v5\developer\adapter_packs\commander\Commander.exe`

**Linux/macOS:**
- `/opt/SimplicityStudio_v5/developer/adapter_packs/commander/Commander`
- `/opt/SimplicityStudio_v4/developer/adapter_packs/commander/Commander`
- `/Applications/Simplicity Studio.app/Contents/Eclipse/developer/adapter_packs/commander/Commander`

### 2. Enhanced Error Handling
- Detailed error messages when Commander is not found
- Execution verification to ensure Commander can actually run
- Permission-specific error detection and guidance

### 3. New Menu Features
Added **Tools** menu with:
- **Check Commander Status**: Verify Commander installation and functionality
- **Set Commander Path**: Manually specify Commander location
- **Test Device Connection**: Check device connectivity and permissions
- **Refresh Commander**: Re-scan for Commander installation
- **Restart as Administrator** (Windows only): Restart with elevated privileges

### 4. Status Bar
Shows current status including:
- Commander availability
- Administrator privileges (Windows)

### 5. Permission Handling
- Detects if running as administrator on Windows
- Provides option to restart with elevated privileges
- Specific guidance for permission-related errors

## How to Resolve Access Issues

### Step 1: Verify Commander Installation
1. Use **Tools > Check Commander Status** to verify installation
2. If not found, install Simplicity Studio or use **Tools > Set Commander Path**

### Step 2: Test Device Connection
1. Connect your Zigbee device via J-Link
2. Use **Tools > Test Device Connection** to verify connectivity
3. Follow any error messages and recommendations

### Step 3: Handle Permission Issues
If you encounter permission errors:

**Option A: Run as Administrator**
1. Use **Tools > Restart as Administrator** (Windows)
2. Or right-click the application and select "Run as administrator"

**Option B: Check Device Usage**
1. Close other applications that might be using the device
2. Disconnect and reconnect the device
3. Ensure J-Link drivers are properly installed

### Step 4: Verify Setup
1. Status bar should show "Commander available | Running as Administrator"
2. Test device connection should succeed
3. Programming should work without errors

## Troubleshooting Common Issues

### "Commander not found"
- Install Simplicity Studio from Silicon Labs
- Use **Tools > Set Commander Path** to manually specify location
- Download Commander standalone from Silicon Labs community

### "Permission denied" or "Access denied"
- Run application as administrator
- Close other applications using the device
- Check J-Link driver installation
- Try disconnecting and reconnecting device

### "Device not found" or connection errors
- Verify device is connected and powered
- Check correct device type is selected
- Ensure J-Link drivers are installed
- Test with **Tools > Test Device Connection**

### "Failed to program application"
- Verify all above steps are completed
- Check file paths are correct
- Ensure device is not in use by other applications
- Try running as administrator

## Additional Resources

- **Simplicity Studio**: https://www.silabs.com/developers/simplicity-studio
- **Commander Standalone**: https://community.silabs.com/s/article/simplicity-commander
- **Silicon Labs Community**: https://community.silabs.com/

## Files Modified

- `zigbee_programmer.py`: Main application with enhanced commander detection and permission handling
- `test_commander_detection.py`: Test script to verify commander detection logic
- `PERMISSION_GUIDE.md`: This documentation file

## Testing

Run the test script to verify commander detection:
```bash
python test_commander_detection.py
```

The application should now automatically detect Commander and provide clear guidance for any permission issues.