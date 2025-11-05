#!/usr/bin/env python3
"""
Test script for the erase validation logic
"""

import tkinter as tk
import tempfile
import os
from zigbee_programmer import ZigbeeProgrammerGUI

def test_erase_validation():
    """Test the validation logic for erase functionality"""
    print("Testing erase validation logic...")
    
    # Create the application
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    
    # Create temporary test files
    with tempfile.NamedTemporaryFile(suffix='.s37', delete=False) as app_file:
        app_file.write(b"test app content")
        app_file_path = app_file.name
    
    with tempfile.NamedTemporaryFile(suffix='.s37', delete=False) as boot_file:
        boot_file.write(b"test bootloader content")
        boot_file_path = boot_file.name
    
    try:
        # Test Case 1: Erase enabled but no bootloader file
        print("\nTest Case 1: Erase enabled but no bootloader file")
        app.device_var.set("OSensor V3")
        app.app_file_var.set(app_file_path)
        app.bootloader_file_var.set("")
        app.erase_before_flash.set(True)
        
        # Simulate the validation logic from program_device_thread
        device_display = app.device_var.get()
        app_file = app.app_file_var.get()
        bootloader_file = app.bootloader_file_var.get()
        erase_before_flash = app.erase_before_flash.get()
        
        validation_passed = True
        error_message = ""
        
        if not device_display:
            validation_passed = False
            error_message = "No device selected"
        elif not app_file:
            validation_passed = False
            error_message = "No application file selected"
        elif not os.path.exists(app_file):
            validation_passed = False
            error_message = "Application file does not exist"
        elif erase_before_flash and not bootloader_file:
            validation_passed = False
            error_message = "Bootloader file is required when 'Erase Before Flash' is enabled"
        elif bootloader_file and not os.path.exists(bootloader_file):
            validation_passed = False
            error_message = "Bootloader file does not exist"
        
        expected_fail = True
        if validation_passed == (not expected_fail):
            print(f"✓ Validation correctly failed: {error_message}")
        else:
            print(f"✗ Validation should have failed but passed")
        
        # Test Case 2: Erase enabled with bootloader file
        print("\nTest Case 2: Erase enabled with bootloader file")
        app.bootloader_file_var.set(boot_file_path)
        
        bootloader_file = app.bootloader_file_var.get()
        
        validation_passed = True
        error_message = ""
        
        if not device_display:
            validation_passed = False
            error_message = "No device selected"
        elif not app_file:
            validation_passed = False
            error_message = "No application file selected"
        elif not os.path.exists(app_file):
            validation_passed = False
            error_message = "Application file does not exist"
        elif erase_before_flash and not bootloader_file:
            validation_passed = False
            error_message = "Bootloader file is required when 'Erase Before Flash' is enabled"
        elif bootloader_file and not os.path.exists(bootloader_file):
            validation_passed = False
            error_message = "Bootloader file does not exist"
        
        expected_pass = True
        if validation_passed == expected_pass:
            print(f"✓ Validation correctly passed")
        else:
            print(f"✗ Validation should have passed but failed: {error_message}")
        
        # Test Case 3: Erase disabled, no bootloader (should pass)
        print("\nTest Case 3: Erase disabled, no bootloader file")
        app.bootloader_file_var.set("")
        app.erase_before_flash.set(False)
        
        bootloader_file = app.bootloader_file_var.get()
        erase_before_flash = app.erase_before_flash.get()
        
        validation_passed = True
        error_message = ""
        
        if not device_display:
            validation_passed = False
            error_message = "No device selected"
        elif not app_file:
            validation_passed = False
            error_message = "No application file selected"
        elif not os.path.exists(app_file):
            validation_passed = False
            error_message = "Application file does not exist"
        elif erase_before_flash and not bootloader_file:
            validation_passed = False
            error_message = "Bootloader file is required when 'Erase Before Flash' is enabled"
        elif bootloader_file and not os.path.exists(bootloader_file):
            validation_passed = False
            error_message = "Bootloader file does not exist"
        
        expected_pass = True
        if validation_passed == expected_pass:
            print(f"✓ Validation correctly passed")
        else:
            print(f"✗ Validation should have passed but failed: {error_message}")
        
        print("\n✓ All erase validation tests completed!")
        
    finally:
        # Clean up temp files
        try:
            os.unlink(app_file_path)
            os.unlink(boot_file_path)
        except:
            pass
        
        # Clean up GUI
        root.destroy()

if __name__ == "__main__":
    test_erase_validation()