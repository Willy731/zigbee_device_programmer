#!/usr/bin/env python3
"""
Test script to verify the device mapping menu functionality
"""

import tkinter as tk
import json
import os
import tempfile
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zigbee_programmer import ZigbeeProgrammerGUI

def test_menu_functionality():
    """Test the device mapping menu functionality"""
    print("Testing device mapping menu functionality...")
    
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    
    try:
        # Test 1: Check initial state
        print("\nTest 1: Initial application state")
        print(f"[OK] Initial device count: {len(app.device_mapping)}")
        print(f"[OK] Initial devices: {list(app.device_mapping.keys())}")
        print(f"[OK] Custom mapping path: {app.custom_mapping_path}")
        
        # Test 2: Create custom mapping and simulate menu selection
        print("\nTest 2: Simulating custom mapping file selection")
        
        custom_mapping = {
            "Menu Test Device 1": "MenuChip1",
            "Menu Test Device 2": "MenuChip2",
            "Menu Test Device 3": "MenuChip3"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(custom_mapping, temp_file, indent=2)
            test_file_path = temp_file.name
        
        # Simulate the file selection process
        original_device_count = len(app.device_mapping)
        
        # Load the custom mapping
        app.custom_mapping_path = test_file_path
        with open(test_file_path, 'r') as f:
            app.device_mapping = json.load(f)
        
        app.device_display_names = list(app.device_mapping.keys())
        app.refresh_device_dropdown()
        app.save_settings()
        
        print(f"[OK] Custom mapping applied: {len(app.device_mapping)} devices")
        print(f"[OK] New devices: {list(app.device_mapping.keys())}")
        
        # Test 3: Check dropdown was updated
        print("\nTest 3: Dropdown update verification")
        dropdown_values = list(app.device_combo['values'])
        print(f"[OK] Dropdown values: {dropdown_values}")
        assert dropdown_values == list(app.device_mapping.keys()), "Dropdown not updated correctly"
        
        # Test 4: Status bar update
        print("\nTest 4: Status bar update")
        app.update_status()
        status_text = app.status_var.get()
        print(f"[OK] Status bar: {status_text}")
        assert "Custom mapping:" in status_text, "Status bar not showing custom mapping"
        
        # Test 5: Persistence check
        print("\nTest 5: Settings persistence verification")
        
        # Create new instance to verify persistence
        root2 = tk.Tk()
        app2 = ZigbeeProgrammerGUI(root2)
        
        print(f"[OK] New instance mapping path: {app2.custom_mapping_path}")
        print(f"[OK] New instance device count: {len(app2.device_mapping)}")
        print(f"[OK] New instance devices: {list(app2.device_mapping.keys())}")
        
        # Verify the custom mapping persisted
        assert app2.custom_mapping_path == test_file_path, "Custom mapping path not persisted"
        assert len(app2.device_mapping) == 3, "Custom mapping not loaded in new instance"
        
        root2.destroy()
        
        print("\n[PASS] All menu functionality tests passed!")
        
    finally:
        # Clean up
        try:
            if 'test_file_path' in locals():
                os.unlink(test_file_path)
        except:
            pass
        root.destroy()

def test_default_file_creation():
    """Test that default device mapping file is created if missing"""
    print("\nTesting default file creation...")
    
    # Temporarily rename the default file if it exists
    default_file = "device_mapping.json"
    backup_file = "device_mapping.json.backup"
    file_existed = False
    
    try:
        if os.path.exists(default_file):
            os.rename(default_file, backup_file)
            file_existed = True
        
        # Create application - should create default file
        root = tk.Tk()
        app = ZigbeeProgrammerGUI(root)
        root.destroy()
        
        # Check if default file was created
        if os.path.exists(default_file):
            print("[OK] Default device mapping file created successfully")
            
            # Verify content
            with open(default_file, 'r') as f:
                mapping = json.load(f)
            print(f"[OK] Default file contains {len(mapping)} devices")
        else:
            print("[X] Default device mapping file was not created")
            
    finally:
        # Restore original file if it existed
        if file_existed and os.path.exists(backup_file):
            if os.path.exists(default_file):
                os.remove(default_file)
            os.rename(backup_file, default_file)

if __name__ == "__main__":
    test_menu_functionality()
    test_default_file_creation()
    print("\n[SUCCESS] All menu tests completed successfully!")