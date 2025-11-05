#!/usr/bin/env python3
"""
Test script to verify log output expansion functionality
"""

import tkinter as tk
import sys
import os
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from zigbee_programmer import ZigbeeProgrammerGUI

def test_log_expansion():
    """Test log output expansion behavior"""
    
    # Create main window
    root = tk.Tk()
    
    # Create the GUI
    app = ZigbeeProgrammerGUI(root)
    
    # Add test messages to demonstrate log expansion
    app.log("=== Log Output Expansion Test ===")
    app.log("Testing vertical expansion of log output area")
    app.log("The log should expand to fill the available vertical space")
    app.log("When you resize the window, the log area should resize with it")
    app.log("")
    app.log("Instructions for manual testing:")
    app.log("1. Resize the window vertically (make it taller/shorter)")
    app.log("2. Verify that the log output area expands/contracts")
    app.log("3. Check that the left panel (Target Device, Application File) stays the same size")
    app.log("4. Ensure the log text area fills the available space")
    app.log("")
    
    # Add more log entries to test scrolling
    for i in range(20):
        app.log(f"Test log entry {i + 1} - This should demonstrate scrolling behavior")
    
    app.log("")
    app.log("=== Test Complete ===")
    app.log("Log output should now be expanding vertically!")
    
    # Display window geometry information
    def show_geometry():
        geometry = root.geometry()
        app.log(f"Current window geometry: {geometry}")
        root.after(5000, show_geometry)  # Update every 5 seconds
    
    root.after(1000, show_geometry)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    test_log_expansion()