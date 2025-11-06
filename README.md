# Zigbee Device Programmer

A GUI application to program Zigbee devices using Simplicity Commander.

## Device Selection

The application provides a user-friendly device selection system:

### Custom Device Names
- **Occupancy Sensor** → `MGM240PB22VNA`
- **Light V2** → `MGM24B02F1024GA` 
- **TestSensor** → `MGM220SC22HNA`
- **Development Board** → `BRD4001A`

The dropdown shows friendly names while the actual chip names are used internally for commander calls. This makes device selection more intuitive while maintaining compatibility with the underlying hardware.

## Features

- **Device Selection**: Choose from a dropdown list of user-friendly device names (Occupancy Sensor, Multi-Sensor, Light V1, Light V2)
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

## Easy Installation (No Python Required)

**For users without Python installed**: Simply double-click `install_python_runner.bat`

This automated installer will:
- ✅ Check if Python is already installed
- ✅ Download and install Python 3.12 automatically
- ✅ Install all required packages
- ✅ Set up the complete environment
- ✅ No administrator privileges required

See [PYTHON_INSTALLATION_GUIDE.md](PYTHON_INSTALLATION_GUIDE.md) for detailed instructions and troubleshooting.

## Manual Installation

### For Users With Python Already Installed

1. Clone the repository:
```bash
git clone https://github.com/Willy731/zigbee_device_programmer.git
cd zigbee_device_programmer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### For Users Without Python

**Option 1: Automated Installation (Recommended)**
- Double-click `install_python_runner.bat`
- Follow the on-screen instructions
- Python and all dependencies will be installed automatically

**Option 2: Manual Python Installation**
1. Download Python 3.12+ from [python.org](https://www.python.org/downloads/)
2. Install Python (make sure to check "Add to PATH")
3. Clone this repository
4. Run: `pip install -r requirements.txt`

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

## Testing

The project includes a comprehensive test suite located in the `tests/` directory:

### Running Tests

1. **Run all tests**:
```bash
python run_tests.py
```

2. **Run individual tests**:
```bash
cd tests
python test_device_mapping_json.py
python test_erase_validation.py
# ... etc
```

### Test Categories

- **Unit Tests**: Core functionality testing
  - `test_zigbee_programmer.py` - Main application tests
  - `test_device_mapping.py` - Device mapping logic
  - `test_version_parsing.py` - Version parsing algorithms
  - `test_filename_extraction.py` - Filename version extraction
  - `test_commander_detection.py` - Commander path detection

- **Integration Tests**: End-to-end functionality
  - `test_integration.py` - Full programming workflow
  - `test_actual_verification.py` - Version verification
  - `test_version_comparison.py` - Version comparison logic
  - `test_exact_scenario.py` - Specific use cases

- **GUI Tests**: User interface and interaction testing
  - `test_debug_mode.py` - Debug mode functionality
  - `test_erase_checkbox.py` - Erase checkbox behavior
  - `test_erase_validation.py` - Erase validation logic
  - `test_program_button.py` - Program button state management
  - `test_comprehensive_button.py` - Complete button workflow
  - `test_device_mapping_json.py` - JSON device mapping
  - `test_menu_functionality.py` - Menu operations

- **Debug and Demo Files**: Development utilities
  - `debug_colors.py` - Color debugging utility
  - `demo_fix.py` - Demonstration fixes
  - `demo_version_comparison.py` - Version comparison examples

### Test Results

All 16 tests currently pass, providing comprehensive coverage of:
- ✅ Core functionality validation
- ✅ Edge case handling  
- ✅ Error condition testing
- ✅ User workflow simulation
- ✅ Integration between components

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