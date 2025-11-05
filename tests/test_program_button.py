#!/usr/bin/env python3
"""
Test script for the dynamic Program Device button functionality
"""

import tkinter as tk
import tempfile
import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zigbee_programmer import ZigbeeProgrammerGUI

def test_program_button_states():
    """Test the dynamic enable/disable of the Program Device button"""
    print("Testing Program Device button enable/disable logic...")
    
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
        # Test Case 1: Initial state (no files selected, erase disabled)
        print("\nTest Case 1: Initial state")
        button_state = str(app.program_button.cget('state'))
        print(f"[OK] Initial button state: {button_state}")
        assert button_state == 'disabled', f"Expected disabled, got {button_state}"
        
        # Test Case 2: Only app file selected, erase disabled
        print("\nTest Case 2: App file selected, erase disabled")
        app.app_file_var.set(app_file_path)
        app.update_program_button_state()
        button_state = str(app.program_button.cget('state'))
        print(f"[OK] Button state with app file: {button_state}")
        assert button_state == 'normal', f"Expected normal, got {button_state}"
        
        # Test Case 3: App file selected, erase enabled, no bootloader
        print("\nTest Case 3: App file selected, erase enabled, no bootloader")
        app.erase_before_flash.set(True)
        app.update_program_button_state()
        button_state = str(app.program_button.cget('state'))
        print(f"[OK] Button state with erase enabled, no bootloader: {button_state}")
        assert button_state == 'disabled', f"Expected disabled, got {button_state}"
        
        # Test Case 4: App file selected, erase enabled, bootloader selected
        print("\nTest Case 4: App file selected, erase enabled, bootloader selected")
        app.bootloader_file_var.set(boot_file_path)
        app.update_program_button_state()
        button_state = str(app.program_button.cget('state'))
        print(f"[OK] Button state with both files and erase enabled: {button_state}")
        assert button_state == 'normal', f"Expected normal, got {button_state}"
        
        # Test Case 5: Remove app file, should disable button
        print("\nTest Case 5: Remove app file")
        app.app_file_var.set("")
        app.update_program_button_state()
        button_state = str(app.program_button.cget('state'))
        print(f"[OK] Button state with no app file: {button_state}")
        assert button_state == 'disabled', f"Expected disabled, got {button_state}"
        
        # Test Case 6: Restore app file, remove bootloader, disable erase
        print("\nTest Case 6: App file restored, no bootloader, erase disabled")
        app.app_file_var.set(app_file_path)
        app.bootloader_file_var.set("")
        app.erase_before_flash.set(False)
        app.update_program_button_state()
        button_state = str(app.program_button.cget('state'))
        print(f"[OK] Button state with app file only, erase disabled: {button_state}")
        assert button_state == 'normal', f"Expected normal, got {button_state}"
        
        # Test Case 7: Test with non-existent file path
        print("\nTest Case 7: Non-existent file path")
        app.app_file_var.set("/nonexistent/file.s37")
        app.update_program_button_state()
        button_state = str(app.program_button.cget('state'))
        print(f"[OK] Button state with non-existent file: {button_state}")
        assert button_state == 'disabled', f"Expected disabled, got {button_state}"
        
        print("\n[PASS] All Program Device button tests passed!")
        
    finally:
        # Clean up temp files
        try:
            os.unlink(app_file_path)
            os.unlink(boot_file_path)
        except:
            pass
        
        # Clean up GUI
        root.destroy()

def test_integration_with_file_dialogs():
    """Test that button state updates when files are selected through dialogs"""
    print("\nTesting integration with file selection...")
    
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    
    # Create temporary test files
    with tempfile.NamedTemporaryFile(suffix='.s37', delete=False) as app_file:
        app_file.write(b"test app content")
        app_file_path = app_file.name
    
    try:
        # Simulate file selection (without actually opening dialog)
        print("Simulating app file selection...")
        app.app_file_var.set(app_file_path)
        app.update_program_button_state()
        
        button_state = str(app.program_button.cget('state'))
        print(f"[OK] Button state after app file selection: {button_state}")
        assert button_state == 'normal', f"Expected normal, got {button_state}"
        
        print("[PASS] Integration test passed!")
        
    finally:
        try:
            os.unlink(app_file_path)
        except:
            pass
        root.destroy()

if __name__ == "__main__":
    test_program_button_states()
    test_integration_with_file_dialogs()
    print("\n[SUCCESS] All tests completed successfully!")