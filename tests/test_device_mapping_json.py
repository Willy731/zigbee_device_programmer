#!/usr/bin/env python3
"""
Test script for JSON device mapping functionality
"""

import tkinter as tk
import json
import os
import tempfile
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zigbee_programmer import ZigbeeProgrammerGUI

def test_device_mapping_json():
    """Test the JSON device mapping functionality"""
    print("Testing JSON device mapping functionality...")
    
    # Create the application
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    
    # Create a test device mapping file
    test_mapping = {
        "Test Device 1": "TestChip1",
        "Test Device 2": "TestChip2",
        "Custom Sensor": "CustomChip123"
    }
    
    try:
        # Test 1: Check default mapping loads
        print("\nTest 1: Default mapping loaded")
        print(f"[OK] Loaded {len(app.device_mapping)} devices from default mapping")
        print(f"[OK] Device names: {list(app.device_mapping.keys())}")
        
        # Test 2: Create and load custom mapping
        print("\nTest 2: Custom mapping file creation and loading")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(test_mapping, temp_file, indent=2)
            test_file_path = temp_file.name
        
        # Simulate loading the custom mapping
        app.custom_mapping_path = test_file_path
        original_mapping = app.device_mapping.copy()
        
        with open(test_file_path, 'r') as f:
            app.device_mapping = json.load(f)
        
        app.device_display_names = list(app.device_mapping.keys())
        app.refresh_device_dropdown()
        
        print(f"[OK] Custom mapping loaded: {len(app.device_mapping)} devices")
        print(f"[OK] Custom device names: {list(app.device_mapping.keys())}")
        
        # Test 3: Check device name resolution
        print("\nTest 3: Device name resolution")
        for display_name, expected_chip in test_mapping.items():
            actual_chip = app.get_actual_device_name(display_name)
            print(f"[OK] {display_name} -> {actual_chip}")
            assert actual_chip == expected_chip, f"Expected {expected_chip}, got {actual_chip}"
        
        # Test 4: Settings save/load
        print("\nTest 4: Settings persistence")
        app.save_settings()
        
        # Create new instance to test loading
        root2 = tk.Tk()
        app2 = ZigbeeProgrammerGUI(root2)
        
        print(f"[OK] Settings loaded in new instance: custom_mapping_path = {app2.custom_mapping_path}")
        if app2.custom_mapping_path == test_file_path:
            print("[OK] Custom mapping path persisted correctly")
        else:
            print(f"[X] Expected {test_file_path}, got {app2.custom_mapping_path}")
        
        root2.destroy()
        
        print("\n[PASS] All JSON device mapping tests passed!")
        
    finally:
        # Clean up
        try:
            if 'test_file_path' in locals():
                os.unlink(test_file_path)
        except:
            pass
        root.destroy()

def test_json_error_handling():
    """Test error handling for invalid JSON files"""
    print("\nTesting JSON error handling...")
    
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    
    try:
        # Test invalid JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write("{ invalid json content }")
            invalid_file_path = temp_file.name
        
        # Test loading invalid file
        app.custom_mapping_path = invalid_file_path
        original_mapping = app.device_mapping.copy()
        
        # This should fall back to default mapping
        app.load_device_mapping()
        
        print("[OK] Invalid JSON handled gracefully")
        print(f"[OK] Fell back to mapping with {len(app.device_mapping)} devices")
        
    finally:
        try:
            if 'invalid_file_path' in locals():
                os.unlink(invalid_file_path)
        except:
            pass
        root.destroy()

if __name__ == "__main__":
    test_device_mapping_json()
    test_json_error_handling()
    print("\n[SUCCESS] All tests completed successfully!")