# Zigbee Device Programmer

A GUI application to program Zigbee devices using Simplicity Commander.

## Device Selection

The application provides a user-friendly device selection system:

### Custom Device Names
- **OSensor V3** → `MGM220PC22HNA`
- **MSensor V2** → `MGM220PC22HNA` 
- **MSensor V1** → `MGM210PA22JIA`
- **ESensor** → `MGM13P02F512GA`

The dropdown shows friendly names while the actual chip names are used internally for commander calls. This makes device selection more intuitive while maintaining compatibility with the underlying hardware.

## Features

- **Device Selection**: Choose from a dropdown list of user-friendly device names (OSensor V3, MSensor V2, MSensor V1, ESensor)
- **Application Programming**: Select and flash application firmware files
- **Bootloader Programming**: Optionally flash bootloader files
- **Real-time Logging**: View command output and programming progress
- **Version Verification**: Automatically verify application version after programming
- **Hex to Version Parsing**: Converts hex version values to readable format (e.g., 0x01010005 → 1.1.5)
- **Commander Auto-Detection**: Automatically finds Simplicity Commander installation
- **Permission Management**: Handles administrator privileges and device access
- **Device Connection Testing**: Test device connectivity before programming

## Prerequisites

1. **Simplicity Commander**: Install Silicon Labs Simplicity Commander and ensure it's in your system PATH
   - Download from: https://www.silabs.com/developers/mcu-programming-options
   
2. **Python 3**: Python 3.6 or later with tkinter support
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On Fedora: `sudo dnf install python3-tkinter`
   - On macOS/Windows: tkinter is usually included with Python

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Willy731/zigbee_device_programmer.git
cd zigbee_device_programmer
```

2. No additional Python packages are required (uses only standard library)

## Usage

1. Run the application:
```bash
python3 zigbee_programmer.py
```

2. In the GUI:
   - Select your device from the dropdown menu
   - Browse and select your application firmware file (.bin, .hex, or .s37)
   - Optionally, browse and select a bootloader file
   - Click "Program Device" to start the programming process
   - Monitor the log output for progress and results

3. The application will:
   - Flash the bootloader (if provided)
   - Flash the application firmware
   - Read device memory and verify the application version
   - Parse hex version values to readable format (e.g., 0x01010005 → 1.1.5)
   - Display the verification results in the log

## Advanced Features

### Version Parsing
The application automatically converts hex version values to readable format:
- **Byte-structured parsing**: `0x01010005` → `1.1.5` (major.minor.patch)
- **Integer math parsing**: Decimal `1001005` → `1.1.5` (calculated as major*1000000 + minor*1000 + patch)
- **Multiple format support**: Handles various hex formats and decimal values

### Filename Version Comparison
The application now compares device versions against the expected version from the filename:
- **Automatic extraction**: Extracts version from filenames like `app_2-1-7.ota` or `occupancy_v3_1-1-5.s37` → `1.1.5`
- **Smart parsing selection**: Uses integer math parsing when available for more accurate version comparison
- **First version validation**: Only validates the FIRST app version found on the device
- **Clear verification**: Displays ✓ VERSION MATCH or ✗ VERSION MISMATCH in the log
- **Pattern support**: Supports various filename patterns like:
  - `msensor_2-1-7.ota` → `2.1.7`
  - `occupancy_v3_1-1-5.s37` → `1.1.5` (underscore format)
  - `C:/path/application_10-20-30.hex` → `10.20.30`

### Tools Menu
- **Check Commander Status**: Verify Simplicity Commander installation and functionality
- **Set Commander Path**: Manually specify Commander executable location  
- **Test Device Connection**: Check device connectivity and permissions
- **Refresh Commander**: Re-scan for Commander installation
- **Restart as Administrator**: Restart with elevated privileges (Windows only)

### Troubleshooting Tools
- Real-time status bar showing Commander availability and admin status
- Comprehensive error messages with specific guidance
- Automatic detection of common installation paths
- Permission verification and guidance

## Supported Devices

The application includes common Zigbee devices such as:
- EFR32MG12P432F1024GL125
- EFR32MG13P632F512GM48
- EFR32MG21A020F1024IM32
- EFR32MG24B210F1536IM48
- EFR32MG24B220F1536IM48
- EFR32MG24B310F1536IM48
- EFR32FG14P233F256GM48
- EFR32FG23A010F512GM48
- EFR32FG25B220F1920IM56

## Commander Commands Used

The application uses the following Simplicity Commander commands:

- **Flash firmware**: `commander flash <file> --device <device>`
- **Read memory**: `commander readmem --region @mainflash --outfile device_dump.bin --device <device>`
- **Get app info**: `commander util appinfo device_dump.bin`

## Troubleshooting

- **"commander not found" error**: 
  - Use "Tools > Check Commander Status" to verify installation
  - Try "Tools > Set Commander Path" to manually specify location
  - Install Simplicity Studio or Commander standalone
- **Permission errors**: 
  - Use "Tools > Restart as Administrator" (Windows)
  - Ensure J-Link drivers are properly installed
- **Device not detected**: 
  - Use "Tools > Test Device Connection" to diagnose issues
  - Check device power and USB connection
  - Verify correct device type selection
- **Programming failed**: 
  - Check the detailed log output for specific error messages
  - Ensure device is not in use by other applications
  - Try disconnecting and reconnecting the device

## Version Parsing Examples

The application converts hex version values and compares them with filename versions:

### Filename Version Extraction:
- `msensor_2-1-7.ota` → `2.1.7` (decimal: 2001007)
- `occupancy_v3_1-1-5.s37` → `1.1.5` (decimal: 1001005) - underscore format
- `C:/path/app_10-20-30.hex` → `10.20.30` (decimal: 10020030)

### Device Version Parsing:
- `0x02010007` → `2.1.7` (byte parsing: 02.01.00.07)
- `0x03010005` → `3.1.5` (byte parsing: 03.01.00.05)
- `0x0A141E00` → `10.20.30.0` (byte parsing: 0A.14.1E.00)

### Version Comparison Results:
```
>>> App version                     : 0x000f462d <<<
>>> Parsed Version: 0.15.70.45 (decimal: 1001005) <<<
>>> ✗ VERSION MISMATCH: Expected 1.1.5 but device has 0.15.70.45 <<<
>>> App version                     : 0x02040002 <<<
>>> Parsed Version: 2.4.2 (decimal: 33816578) <<<
>>> (Secondary app version - not validated) <<<
>>> ✗ VERSION VERIFICATION FAILED: Device version does not match filename! <<<
```

## License

This project is open source and available for use and modification.