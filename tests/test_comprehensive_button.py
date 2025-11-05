#!/usr/bin/env python3
"""
Comprehensive test for the complete erase checkbox and button state integration
"""

import tkinter as tk
import tempfile
import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zigbee_programmer import ZigbeeProgrammerGUI

def test_complete_workflow():
    """Test the complete workflow from user perspective"""
    print("Testing complete workflow integration...")
    
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
        print("\n=== Testing User Workflow ===")
        
        # Step 1: User starts with empty form
        print("1. Initial state:")
        print(f"   - Program button: {str(app.program_button.cget('state'))}")
        print(f"   - Erase checkbox: {app.erase_before_flash.get()}")
        print(f"   - Bootloader label: {app.bootloader_optional_label.cget('text')}")
        assert str(app.program_button.cget('state')) == 'disabled'
        
        # Step 2: User selects application file
        print("\n2. User selects application file:")
        app.app_file_var.set(app_file_path)
        app.update_program_button_state()
        print(f"   - Program button: {str(app.program_button.cget('state'))}")
        assert str(app.program_button.cget('state')) == 'normal'
        
        # Step 3: User checks "Erase Before Flash"
        print("\n3. User checks 'Erase Before Flash':")
        app.erase_before_flash.set(True)
        app.on_erase_checkbox_changed()
        print(f"   - Program button: {str(app.program_button.cget('state'))}")
        print(f"   - Bootloader label: {app.bootloader_optional_label.cget('text')}")
        print(f"   - Label color: {app.bootloader_optional_label.cget('foreground')}")
        assert str(app.program_button.cget('state')) == 'disabled'
        assert app.bootloader_optional_label.cget('text') == "(Required for Erase)"
        assert str(app.bootloader_optional_label.cget('foreground')) == "red"
        
        # Step 4: User selects bootloader file
        print("\n4. User selects bootloader file:")
        app.bootloader_file_var.set(boot_file_path)
        app.update_program_button_state()
        print(f"   - Program button: {str(app.program_button.cget('state'))}")
        assert str(app.program_button.cget('state')) == 'normal'
        
        # Step 5: User unchecks "Erase Before Flash"
        print("\n5. User unchecks 'Erase Before Flash':")
        app.erase_before_flash.set(False)
        app.on_erase_checkbox_changed()
        print(f"   - Program button: {str(app.program_button.cget('state'))}")
        print(f"   - Bootloader label: {app.bootloader_optional_label.cget('text')}")
        print(f"   - Label color: {app.bootloader_optional_label.cget('foreground')}")
        assert str(app.program_button.cget('state')) == 'normal'
        assert app.bootloader_optional_label.cget('text') == "(Optional)"
        assert str(app.bootloader_optional_label.cget('foreground')) == "black"
        
        # Step 6: User removes bootloader file (should still work since erase is off)
        print("\n6. User removes bootloader file (erase still off):")
        app.bootloader_file_var.set("")
        app.update_program_button_state()
        print(f"   - Program button: {str(app.program_button.cget('state'))}")
        assert str(app.program_button.cget('state')) == 'normal'
        
        # Step 7: User checks erase again (should disable since no bootloader)
        print("\n7. User checks erase again (no bootloader):")
        app.erase_before_flash.set(True)
        app.on_erase_checkbox_changed()
        print(f"   - Program button: {str(app.program_button.cget('state'))}")
        assert str(app.program_button.cget('state')) == 'disabled'
        
        print("\n[PASS] Complete workflow test passed!")
        
    finally:
        try:
            os.unlink(app_file_path)
            os.unlink(boot_file_path)
        except:
            pass
        root.destroy()

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\nTesting edge cases...")
    
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    
    try:
        # Test with empty string paths
        print("Testing empty string paths...")
        app.app_file_var.set("")
        app.bootloader_file_var.set("")
        app.erase_before_flash.set(True)
        app.update_program_button_state()
        assert str(app.program_button.cget('state')) == 'disabled'
        
        # Test with whitespace-only paths
        print("Testing whitespace-only paths...")
        app.app_file_var.set("   ")
        app.bootloader_file_var.set("  ")
        app.update_program_button_state()
        assert str(app.program_button.cget('state')) == 'disabled'
        
        print("[PASS] Edge cases test passed!")
        
    finally:
        root.destroy()

if __name__ == "__main__":
    test_complete_workflow()
    test_edge_cases()
    print("\n[SUCCESS] All comprehensive tests completed successfully!")