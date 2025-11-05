#!/usr/bin/env python3
"""
Test script for complete version comparison functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_version_comparison():
    """Test the complete version comparison functionality"""
    
    # Import from the main module
    try:
        from zigbee_programmer import ZigbeeProgrammerGUI
        import tkinter as tk
    except ImportError as e:
        print(f"Error importing: {e}")
        return
    
    # Create a minimal test instance
    root = tk.Tk()
    root.withdraw()  # Hide the window
    app = ZigbeeProgrammerGUI(root)
    
    print("=" * 70)
    print("Version Comparison Test")
    print("=" * 70)
    
    # Test cases: (filename, device_hex_version, should_match)
    test_cases = [
        ("msensor_2-1-7.ota", "0x02010007", True),   # Should match: 2.1.7
        ("occupancy_3-1-5.s37", "0x03010005", True), # Should match: 3.1.5
        ("app_1-0-3.hex", "0x01000003", True),       # Should match: 1.0.3
        ("firmware_2-1-7.bin", "0x01020003", False), # Should NOT match: different versions
        ("test_10-20-30.ota", "0x0A141E00", True),   # Should match: 10.20.30 (hex: 0A=10, 14=20, 1E=30)
    ]
    
    for i, (filename, hex_version, should_match) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {filename} vs {hex_version}")
        print("-" * 50)
        
        # Extract version from filename
        file_version, file_decimal = app.extract_version_from_filename(filename)
        print(f"Filename version: {file_version} (decimal: {file_decimal})")
        
        # Parse device version
        device_line = f"App version: {hex_version}"
        original, device_version, device_decimal = app.parse_app_version(device_line)
        print(f"Device version:   {device_version} (decimal: {device_decimal})")
        
        # Check if they match
        if file_version and device_version:
            # Enhanced matching logic (same as in the main application)
            decimal_match = (file_decimal == device_decimal)
            string_match = (file_version == device_version)
            
            # Handle trailing .0 cases
            trailing_zero_match = False
            if device_version.endswith('.0') and device_version[:-2] == file_version:
                trailing_zero_match = True
            elif file_version.endswith('.0') and file_version[:-2] == device_version:
                trailing_zero_match = True
            
            any_match = decimal_match or string_match or trailing_zero_match
            
            print(f"Decimal match:    {decimal_match}")
            print(f"String match:     {string_match}")
            print(f"Trailing .0 match: {trailing_zero_match}")
            print(f"Overall result:   {'MATCH' if any_match else 'NO MATCH'}")
            print(f"Expected result:  {'MATCH' if should_match else 'NO MATCH'}")
            print(f"Test result:      {'✓ PASS' if (any_match == should_match) else '✗ FAIL'}")
        else:
            print("Could not parse one or both versions")
            print(f"Test result:      {'✗ FAIL' if should_match else '? INCONCLUSIVE'}")
    
    # Test edge cases
    print(f"\n{'=' * 70}")
    print("Edge Cases")
    print("=" * 70)
    
    edge_cases = [
        ("no_version_file.ota", "0x01020003", "No version in filename"),
        ("version_1-2-3.hex", "Invalid device version", "Invalid device version"),
        ("C:/long/path/to/app_5-6-7.bin", "0x05060007", "Full path with version"),
    ]
    
    for filename, device_input, description in edge_cases:
        print(f"\nEdge case: {description}")
        print(f"File: {filename}")
        print(f"Device: {device_input}")
        
        file_version, file_decimal = app.extract_version_from_filename(filename)
        print(f"File result: {file_version if file_version else 'NO VERSION'}")
        
        if "Invalid" not in device_input:
            device_line = f"App version: {device_input}"
            original, device_version, device_decimal = app.parse_app_version(device_line)
            print(f"Device result: {device_version if device_version else 'NO VERSION'}")
        else:
            print("Device result: INVALID INPUT")
    
    root.destroy()
    print(f"\n{'=' * 70}")
    print("Version comparison tests completed!")

if __name__ == "__main__":
    test_version_comparison()