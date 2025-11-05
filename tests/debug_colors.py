#!/usr/bin/env python3
"""
Debug test to check color values
"""

import tkinter as tk
from zigbee_programmer import ZigbeeProgrammerGUI

def debug_colors():
    """Debug the color values returned by tkinter"""
    print("Debugging color values...")
    
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    
    try:
        # Check initial color
        initial_color = app.bootloader_optional_label.cget('foreground')
        print(f"Initial color: '{initial_color}' (type: {type(initial_color)})")
        print(f"Initial color repr: {repr(initial_color)}")
        
        # Check color after enabling erase
        app.erase_before_flash.set(True)
        app.on_erase_checkbox_changed()
        red_color = app.bootloader_optional_label.cget('foreground')
        print(f"Red color: '{red_color}' (type: {type(red_color)})")
        print(f"Red color repr: {repr(red_color)}")
        
        # Check color after disabling erase
        app.erase_before_flash.set(False)
        app.on_erase_checkbox_changed()
        black_color = app.bootloader_optional_label.cget('foreground')
        print(f"Black color: '{black_color}' (type: {type(black_color)})")
        print(f"Black color repr: {repr(black_color)}")
        
    finally:
        root.destroy()

if __name__ == "__main__":
    debug_colors()