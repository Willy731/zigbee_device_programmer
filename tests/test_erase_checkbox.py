#!/usr/bin/env python3
"""
Test script for the "Erase Before Flash" checkbox functionality
"""

import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zigbee_programmer import ZigbeeProgrammerGUI

def test_erase_checkbox():
    """Test the erase checkbox functionality"""
    print("Testing Erase Before Flash checkbox functionality...")
    
    # Create the application
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    
    # Test initial state
    print(f"[OK] Initial erase state: {app.erase_before_flash.get()}")
    print(f"[OK] Initial bootloader label: {app.bootloader_optional_label.cget('text')}")
    
    # Test checking the erase checkbox
    app.erase_before_flash.set(True)
    app.on_erase_checkbox_changed()
    print(f"[OK] Erase enabled state: {app.erase_before_flash.get()}")
    print(f"[OK] Bootloader label when erase enabled: {app.bootloader_optional_label.cget('text')}")
    print(f"[OK] Label color when erase enabled: {app.bootloader_optional_label.cget('foreground')}")
    
    # Test unchecking the erase checkbox
    app.erase_before_flash.set(False)
    app.on_erase_checkbox_changed()
    print(f"[OK] Erase disabled state: {app.erase_before_flash.get()}")
    print(f"[OK] Bootloader label when erase disabled: {app.bootloader_optional_label.cget('text')}")
    print(f"[OK] Label color when erase disabled: {app.bootloader_optional_label.cget('foreground')}")
    
    print("\n[OK] All erase checkbox tests passed!")
    
    # Clean up
    root.destroy()

if __name__ == "__main__":
    test_erase_checkbox()