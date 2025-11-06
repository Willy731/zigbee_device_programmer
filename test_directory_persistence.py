#!/usr/bin/env python3
"""
Test script to verify directory persistence functionality
"""

import os
import json
import tempfile
import tkinter as tk
from tkinter import filedialog

# Import the modules we want to test
from device_manager import DeviceMappingManager
from file_operations import FileOperationsManager

def test_directory_persistence():
    """Test that directory persistence works correctly"""
    print("Testing directory persistence functionality...")
    
    # Create a temporary settings file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_settings_file = temp_file.name
        # Initialize with empty settings
        json.dump({"custom_mapping_path": None}, temp_file)
    
    try:
        # Create device manager with temporary settings file
        device_manager = DeviceMappingManager()
        device_manager.settings_file = temp_settings_file
        device_manager.load_settings()
        
        # Create file operations manager
        file_ops = FileOperationsManager(
            debug_callback=print,
            settings_manager=device_manager
        )
        
        # Test 1: Check initial state
        print("\n1. Testing initial state...")
        initial_settings = device_manager.load_directory_settings()
        print(f"Initial directory settings: {initial_settings}")
        assert initial_settings == {}, "Initial settings should be empty"
        print("✓ Initial state correct")
        
        # Test 2: Simulate setting directories
        print("\n2. Testing directory saving...")
        test_app_dir = "C:\\TestApp"
        test_boot_dir = "C:\\TestBootloader"
        
        # Manually set directories (simulating file selection)
        file_ops._last_app_directory = test_app_dir
        file_ops._last_bootloader_directory = test_boot_dir
        file_ops._save_directory_settings()
        
        # Verify settings were saved
        saved_settings = device_manager.load_directory_settings()
        print(f"Saved directory settings: {saved_settings}")
        assert saved_settings['last_app_directory'] == test_app_dir
        assert saved_settings['last_bootloader_directory'] == test_boot_dir
        print("✓ Directory saving works")
        
        # Test 3: Test loading in new instance
        print("\n3. Testing directory loading...")
        new_device_manager = DeviceMappingManager()
        new_device_manager.settings_file = temp_settings_file
        
        new_file_ops = FileOperationsManager(
            debug_callback=print,
            settings_manager=new_device_manager
        )
        
        # Check if directories were loaded correctly
        assert new_file_ops._last_app_directory == test_app_dir
        assert new_file_ops._last_bootloader_directory == test_boot_dir
        print("✓ Directory loading works")
        
        # Test 4: Check settings file content
        print("\n4. Testing settings file content...")
        with open(temp_settings_file, 'r') as f:
            file_content = json.load(f)
        
        print(f"Settings file content: {json.dumps(file_content, indent=2)}")
        assert 'directory_settings' in file_content
        assert file_content['directory_settings']['last_app_directory'] == test_app_dir
        assert file_content['directory_settings']['last_bootloader_directory'] == test_boot_dir
        print("✓ Settings file format correct")
        
        print("\n🎉 All tests passed! Directory persistence is working correctly.")
        
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_settings_file)
        except:
            pass

def test_initial_directory_logic():
    """Test the initial directory selection logic"""
    print("\nTesting initial directory selection logic...")
    
    # Create device manager and file operations manager
    device_manager = DeviceMappingManager()
    file_ops = FileOperationsManager(
        debug_callback=print,
        settings_manager=device_manager
    )
    
    # Test with no previous directories
    current_dir = os.getcwd()
    initial_dir = file_ops._get_initial_directory("", None)
    print(f"Initial directory with no history: {initial_dir}")
    assert initial_dir == current_dir
    print("✓ Defaults to current directory when no history")
    
    # Test with last directory
    test_dir = "C:\\TestDirectory"
    file_ops._last_app_directory = test_dir
    
    # Since test directory doesn't exist, should fall back to current
    initial_dir = file_ops._get_initial_directory("", test_dir)
    print(f"Initial directory with non-existent last dir: {initial_dir}")
    assert initial_dir == current_dir
    print("✓ Falls back to current directory when last directory doesn't exist")
    
    # Test with current path
    current_file = os.path.abspath(__file__)
    expected_dir = os.path.dirname(current_file)
    initial_dir = file_ops._get_initial_directory(current_file, None)
    print(f"Initial directory with current file: {initial_dir}")
    assert initial_dir == expected_dir
    print("✓ Uses directory of current file when available")
    
    print("🎉 Initial directory logic tests passed!")

if __name__ == "__main__":
    print("=" * 60)
    print("Directory Persistence Test Suite")
    print("=" * 60)
    
    try:
        test_directory_persistence()
        test_initial_directory_logic()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("The directory persistence feature is working correctly.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()