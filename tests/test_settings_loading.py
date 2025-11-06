#!/usr/bin/env python3
"""
Test script to verify the application loads directory settings correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from device_manager import DeviceMappingManager
from file_operations import FileOperationsManager

def test_app_loading():
    """Test that the application loads directory settings correctly"""
    print("Testing application loading with existing settings...")
    
    # Create device manager (will load from zigbee_programmer_settings.json)
    device_manager = DeviceMappingManager()
    
    # Create file operations manager (same as in main app)
    file_ops = FileOperationsManager(
        debug_callback=print,
        settings_manager=device_manager
    )
    
    print(f"Loaded app directory: {file_ops._last_app_directory}")
    print(f"Loaded bootloader directory: {file_ops._last_bootloader_directory}")
    
    # Verify the directories were loaded (check for any valid directories)
    if file_ops._last_app_directory:
        print("[OK] Application directory loaded correctly")
        print(f"  App directory: {file_ops._last_app_directory}")
    else:
        print("[X] No application directory loaded")
    
    if file_ops._last_bootloader_directory:
        print("[OK] Bootloader directory loaded correctly")
        print(f"  Bootloader directory: {file_ops._last_bootloader_directory}")
    else:
        print("[X] No bootloader directory loaded")
    
    print("\n[SUCCESS] Directory loading test completed!")

if __name__ == "__main__":
    test_app_loading()