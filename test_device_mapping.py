#!/usr/bin/env python3
"""
Test script to demonstrate the device mapping functionality
"""

# Import the main class to test the device mapping
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zigbee_programmer import ZigbeeProgrammerGUI
import tkinter as tk

def test_device_mapping():
    """Test the device mapping functionality"""
    print("=== Device Mapping Test ===")
    
    # Create a minimal root for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create the app instance
    app = ZigbeeProgrammerGUI(root)
    
    print("\nDevice Mapping:")
    print("Display Name -> Actual Chip Name")
    print("-" * 40)
    
    for display_name, chip_name in app.device_mapping.items():
        actual_name = app.get_actual_device_name(display_name)
        print(f"{display_name:15} -> {actual_name}")
        
        # Verify the mapping works correctly
        assert actual_name == chip_name, f"Mapping failed for {display_name}"
    
    print("\nAvailable display names for dropdown:")
    for i, name in enumerate(app.device_display_names):
        print(f"  {i+1}. {name}")
    
    # Test fallback behavior
    unknown_device = "Unknown Device"
    fallback_result = app.get_actual_device_name(unknown_device)
    print(f"\nFallback test: '{unknown_device}' -> '{fallback_result}'")
    assert fallback_result == unknown_device, "Fallback behavior failed"
    
    print("\n✓ All device mapping tests passed!")
    
    root.destroy()

if __name__ == "__main__":
    test_device_mapping()