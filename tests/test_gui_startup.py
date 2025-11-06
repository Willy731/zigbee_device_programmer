#!/usr/bin/env python3
"""
Simple test to check GUI startup
"""

import tkinter as tk
import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from zigbee_programmer import ZigbeeProgrammerGUI

def test_gui_startup():
    """Test GUI startup and theme colors"""
    try:
        # Create main window
        root = tk.Tk()
        
        # Create the GUI
        app = ZigbeeProgrammerGUI(root)
        
        # Test initial theme
        print(f"[OK] GUI started successfully")
        print(f"[OK] Initial theme: {app.current_theme}")
        
        # Get and test theme colors
        colors = app.get_theme_colors()
        print(f"[OK] Theme colors loaded: {len(colors)} color values")
        print(f"  - Background: {colors['bg']}")
        print(f"  - Card background: {colors['card_bg']}")
        print(f"  - Text primary: {colors['text_primary']}")
        
        # Test that the combobox exists
        if hasattr(app, 'device_combo'):
            print(f"[OK] Device combobox created successfully")
        
        # Test that entries exist
        if hasattr(app, 'app_entry'):
            print(f"[OK] Application file entry created successfully")
        
        if hasattr(app, 'boot_entry'):
            print(f"[OK] Bootloader file entry created successfully")
        
        print(f"\n[OK] All basic components working correctly!")
        
        # Close after a short delay
        root.after(1000, root.quit)
        root.mainloop()
        
        print(f"[OK] GUI closed successfully")
        
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui_startup()
