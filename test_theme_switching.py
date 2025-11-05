#!/usr/bin/env python3
"""
Test script to verify theme switching functionality
"""

import tkinter as tk
import sys
import os

# Add the current directory to Python path to import our module
sys.path.insert(0, os.path.dirname(__file__))

from zigbee_programmer import ZigbeeProgrammerGUI

def test_theme_switching():
    """Test theme switching functionality"""
    
    # Create main window
    root = tk.Tk()
    
    # Create the GUI
    app = ZigbeeProgrammerGUI(root)
    
    # Test initial theme
    print(f"Initial theme: {app.current_theme}")
    
    # Test getting theme colors
    colors = app.get_theme_colors()
    print(f"Dark theme colors loaded: {list(colors.keys())}")
    
    # Toggle to light theme
    print("\nToggling to light theme...")
    app.toggle_theme()
    print(f"New theme: {app.current_theme}")
    
    # Test light theme colors
    colors = app.get_theme_colors()
    print(f"Light theme background: {colors['bg']}")
    print(f"Light theme card background: {colors['card_bg']}")
    print(f"Light theme text: {colors['text_primary']}")
    
    # Toggle back to dark theme
    print("\nToggling back to dark theme...")
    app.toggle_theme()
    print(f"Final theme: {app.current_theme}")
    
    # Test dark theme colors again
    colors = app.get_theme_colors()
    print(f"Dark theme background: {colors['bg']}")
    print(f"Dark theme card background: {colors['card_bg']}")
    print(f"Dark theme text: {colors['text_primary']}")
    
    print("\nTheme switching test completed successfully!")
    
    # Close the application
    root.after(100, root.quit)
    root.mainloop()

if __name__ == "__main__":
    test_theme_switching()