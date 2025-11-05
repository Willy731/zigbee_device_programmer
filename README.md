# Zigbee Device Programmer

A GUI application to program Zigbee devices using Simplicity Commander.

## Features

- **Device Selection**: Choose from a dropdown list of common Zigbee devices
- **Application Programming**: Select and flash application firmware files
- **Bootloader Programming**: Optionally flash bootloader files
- **Real-time Logging**: View command output and programming progress
- **Version Verification**: Automatically verify application version after programming

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
   - Display the verification results in the log

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

- **"commander not found" error**: Ensure Simplicity Commander is installed and added to your system PATH
- **Device not detected**: Check that your device is properly connected and drivers are installed
- **Programming failed**: Check the log output for specific error messages

## License

This project is open source and available for use and modification.