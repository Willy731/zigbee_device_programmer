# Device Mapping JSON Feature

## Overview
The Zigbee Device Programmer now supports customizable device mappings through JSON files. This allows users to easily add, modify, or customize the device names and their corresponding chip names without modifying the source code.

## Files Created

### 1. `device_mapping.json` (Default mapping file)
```json
{
    "OSensor V3": "MGM220PC22HNA",
    "MSensor V2": "MGM220PC22HNA",
    "MSensor V1": "MGM210PA22JIA",
    "ESensor": "MGM13P02F512GA"
}
```

### 2. `custom_device_mapping.json` (Example custom mapping)
```json
{
    "OSensor V4": "MGM240PB22VNA",
    "MSensor V3": "MGM240PB22VNA",
    "MSensor V2": "MGM220PC22HNA",
    "MSensor V1": "MGM210PA22JIA",
    "ESensor V2": "MGM24B02F1024GA",
    "ESensor V1": "MGM13P02F512GA",
    "TestSensor": "MGM220SC22HNA",
    "Development Board": "BRD4001A"
}
```

### 3. `zigbee_programmer_settings.json` (Auto-generated settings file)
```json
{
  "custom_mapping_path": "/path/to/your/custom_device_mapping.json"
}
```

## Features

### 1. **Automatic Default Loading**
- On first run, the application creates `device_mapping.json` with default mappings
- If this file exists, it's loaded automatically
- If missing or corrupted, falls back to hardcoded defaults

### 2. **Custom Mapping Selection**
- **Menu Option**: `Tools > Select Device Mapping File...`
- Allows selection of any JSON file with device mappings
- Validates JSON format before loading
- Updates device dropdown immediately

### 3. **Persistent Settings**
- Custom mapping file path is saved in `zigbee_programmer_settings.json`
- Setting is automatically restored when application restarts
- No need to re-select custom mapping files

### 4. **Status Bar Integration**
- Shows "Default mapping" when using default file
- Shows "Custom mapping: filename.json" when using custom file
- Provides immediate visual feedback of current mapping source

### 5. **Error Handling**
- Graceful fallback to default mapping if custom file is invalid
- User-friendly error messages for JSON parsing issues
- Automatic recovery from corrupted or missing files

## Usage Instructions

### Creating a Custom Device Mapping

1. **Create a new JSON file** (e.g., `my_devices.json`):
```json
{
    "My Device Name": "ACTUAL_CHIP_NAME",
    "Another Device": "ANOTHER_CHIP_NAME"
}
```

2. **Load the custom mapping**:
   - Open the Zigbee Device Programmer
   - Go to `Tools > Select Device Mapping File...`
   - Browse and select your JSON file
   - The device dropdown will update immediately

3. **Verify the mapping**:
   - Check the status bar shows "Custom mapping: your_file.json"
   - Verify your devices appear in the dropdown
   - Restart the application to confirm persistence

### JSON Format Requirements

- Must be valid JSON
- Must be a single object (dictionary)
- Keys: Display names shown in the dropdown
- Values: Actual chip names passed to commander
- Example:
```json
{
    "User-Friendly Name": "TECHNICAL_CHIP_NAME",
    "Development Board": "BRD4001A",
    "Custom Sensor v1.0": "MGM220PC22HNA"
}
```

## Implementation Details

### Code Changes Made

1. **New Methods Added**:
   - `load_settings()`: Load persistent application settings
   - `save_settings()`: Save settings to JSON file
   - `load_device_mapping()`: Load device mapping from JSON with fallbacks
   - `select_device_mapping_file()`: Menu handler for custom mapping selection
   - `refresh_device_dropdown()`: Update GUI dropdown with new mappings

2. **Modified Methods**:
   - `__init__()`: Added settings file path and JSON loading
   - `create_menu()`: Added device mapping menu option
   - `update_status()`: Show current mapping file in status bar

3. **New Files**:
   - `device_mapping.json`: Default device mappings
   - `custom_device_mapping.json`: Example custom mappings
   - `zigbee_programmer_settings.json`: Auto-generated settings (runtime)

### Loading Priority

1. **Custom mapping file** (if specified in settings and exists)
2. **Default mapping file** (`device_mapping.json`)
3. **Hardcoded fallback** (built into source code)

### Settings Persistence

The application automatically saves/loads:
- Custom device mapping file path
- Other future settings can be added to the same JSON structure

## Testing

Comprehensive tests verify:
- JSON loading and parsing
- Error handling for invalid files
- Settings persistence across application restarts
- Menu functionality and UI updates
- Fallback behavior when files are missing

## Future Enhancements

Potential improvements:
- Device mapping editor GUI
- Import/export functionality
- Multiple mapping profiles
- Online mapping repository
- Validation of chip names against known devices