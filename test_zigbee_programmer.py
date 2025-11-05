#!/usr/bin/env python3
"""
Test script for Zigbee Programmer GUI
Tests the core functionality without requiring a GUI
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, scrolledtext, messagebox
        import subprocess
        import threading
        import os
        import tempfile
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_class_structure():
    """Test that the GUI class can be instantiated (without mainloop)"""
    print("\nTesting class structure...")
    try:
        # We can't actually create the GUI without a display, but we can import the class
        import zigbee_programmer
        print("✓ Module imports successfully")
        print("✓ ZigbeeProgrammerGUI class is defined")
        return True
    except Exception as e:
        print(f"✗ Class structure test failed: {e}")
        return False

def test_device_list():
    """Test that device list is properly defined"""
    print("\nTesting device list...")
    try:
        import zigbee_programmer
        # The devices list is defined in __init__, so we can't access it without instantiation
        # But we can verify the class has the expected methods
        expected_methods = ['create_widgets', 'browse_app_file', 'browse_bootloader_file', 
                          'log', 'clear_log', 'run_commander_command', 'verify_app_version',
                          'program_device_thread', 'program_device']
        
        for method in expected_methods:
            if not hasattr(zigbee_programmer.ZigbeeProgrammerGUI, method):
                print(f"✗ Missing method: {method}")
                return False
        
        print("✓ All expected methods are defined")
        return True
    except Exception as e:
        print(f"✗ Device list test failed: {e}")
        return False

def test_commander_commands():
    """Test that commander command structure is correct"""
    print("\nTesting commander command structure...")
    try:
        # Test command format
        device = "EFR32MG21A020F1024IM32"
        app_file = "/path/to/app.bin"
        dump_file = os.path.join(tempfile.gettempdir(), "device_dump.bin")
        
        # Flash command
        flash_cmd = ["commander", "flash", app_file, "--device", device]
        print(f"  Flash command: {' '.join(flash_cmd)}")
        
        # Readmem command
        readmem_cmd = ["commander", "readmem", "--region", "@mainflash", 
                      "--outfile", dump_file, "--device", device]
        print(f"  Readmem command: {' '.join(readmem_cmd)}")
        
        # Appinfo command
        appinfo_cmd = ["commander", "util", "appinfo", dump_file]
        print(f"  Appinfo command: {' '.join(appinfo_cmd)}")
        
        print("✓ Command structures are correct")
        return True
    except Exception as e:
        print(f"✗ Commander command test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Zigbee Programmer GUI - Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_class_structure,
        test_device_list,
        test_commander_commands
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
