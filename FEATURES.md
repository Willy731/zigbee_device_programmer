# Zigbee Device Programmer - Features

## GUI Components

### 1. Device Selection
- **Dropdown Menu**: Select from 9 pre-configured Zigbee devices
- Supported devices include EFR32MG12, MG13, MG21, MG24, FG14, FG23, and FG25 series

### 2. File Selection
- **Application File Browser**: Select firmware files (.bin, .hex, .s37)
- **Bootloader File Browser**: Optional bootloader selection
- Visual feedback showing selected file paths

### 3. Program Button
- Initiates the programming sequence
- Disabled during programming to prevent multiple operations
- Re-enabled after completion

### 4. Log Window
- **Real-time Output**: Shows all commander commands and their output
- **Scrollable Text**: Auto-scrolls to show latest messages
- **Clear Log Button**: Reset the log window

## Programming Workflow

1. **Device Selection**: Choose the target device from dropdown
2. **File Selection**: Browse and select application firmware (required)
3. **Optional Bootloader**: Select bootloader firmware if needed
4. **Program**: Click "Program Device" to start
5. **Progress Monitoring**: Watch real-time log output
6. **Verification**: Application version is automatically verified

## Commander Integration

### Flash Command
```bash
commander flash <file> --device <device>
```
- Used for both bootloader and application programming

### Read Memory Command
```bash
commander readmem --region @mainflash --outfile device_dump.bin --device <device>
```
- Reads device memory for verification

### Application Info Command
```bash
commander util appinfo device_dump.bin
```
- Extracts and displays application version information

## Key Features

- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux
- ✅ **User-Friendly**: Intuitive GUI with clear labels
- ✅ **Real-time Feedback**: Live command output in log window
- ✅ **Error Handling**: Comprehensive error messages and validation
- ✅ **Threaded Execution**: UI remains responsive during programming
- ✅ **Version Verification**: Automatic app version check after programming
- ✅ **No External Dependencies**: Uses Python standard library only

## Error Handling

The application handles:
- Missing commander executable
- Invalid file paths
- Device connection issues
- Programming failures
- Command timeouts (120 second limit)

All errors are clearly displayed in the log window with descriptive messages.
