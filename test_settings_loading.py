#!/usr/bin/env python3
"""
Test script to verify the application loads directory settings correctly
"""

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
    
    # Verify the directories were loaded
    expected_dir = "S:/Workspaces/zigbee_device_programmer"
    
    if file_ops._last_app_directory == expected_dir:
        print("✓ Application directory loaded correctly")
    else:
        print(f"❌ Application directory mismatch: expected {expected_dir}, got {file_ops._last_app_directory}")
    
    if file_ops._last_bootloader_directory == expected_dir:
        print("✓ Bootloader directory loaded correctly")
    else:
        print(f"❌ Bootloader directory mismatch: expected {expected_dir}, got {file_ops._last_bootloader_directory}")
    
    print("\n🎉 Directory loading test completed!")

if __name__ == "__main__":
    test_app_loading()