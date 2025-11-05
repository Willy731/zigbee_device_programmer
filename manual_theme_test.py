#!/usr/bin/env python3
"""
Manual test to launch GUI and verify theme switching through menu
"""

import tkinter as tk
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from zigbee_programmer import ZigbeeProgrammerGUI

def main():
    """Launch the GUI for manual theme switching test"""
    
    print("=== Manual Theme Switching Test ===")
    print()
    print("Instructions:")
    print("1. The GUI will open in dark theme")
    print("2. Go to View menu > Toggle Dark/Light Theme")
    print("3. Verify that all UI elements switch to light theme:")
    print("   - Background should be white/light gray")
    print("   - Card backgrounds should be light")
    print("   - Text should be dark")
    print("   - 'Target Device' and 'Application File' frames should be light")
    print("4. Toggle back to dark theme and verify all elements are dark")
    print("5. Close the application when testing is complete")
    print()
    print("Starting GUI...")
    
    # Create and run the GUI
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    
    # Add a test message to the log
    app.log("Theme switching test started")
    app.log("Use View menu > Toggle Dark/Light Theme to test theme switching")
    app.log("Verify that all UI components (Target Device, Application File frames) change colors correctly")
    
    root.mainloop()
    
    print("GUI closed. Test complete!")

if __name__ == "__main__":
    main()