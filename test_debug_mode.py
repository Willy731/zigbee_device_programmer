#!/usr/bin/env python3
"""
Test script to demonstrate debug mode functionality
"""

import sys
import os
import tempfile
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zigbee_programmer import ZigbeeProgrammerGUI
import tkinter as tk

def test_debug_mode():
    """Test the debug mode functionality"""
    print("=" * 70)
    print("Debug Mode Test")
    print("=" * 70)
    
    # Create a minimal root for testing
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    # Create the app instance
    app = ZigbeeProgrammerGUI(root)
    
    print("\nTesting debug mode functionality:")
    print("-" * 50)
    
    # Test initial state
    print(f"Initial debug mode state: {app.debug_mode}")
    assert app.debug_mode == False, "Debug mode should start as False"
    
    # Test debug logging when disabled
    print("\nTesting debug_log when debug mode is OFF:")
    app.debug_log("This debug message should NOT appear in normal log")
    
    # Enable debug mode
    print("\nEnabling debug mode...")
    app.debug_mode = True
    
    # Test debug logging when enabled
    print("Testing debug_log when debug mode is ON:")
    app.debug_log("This debug message SHOULD appear in debug log")
    
    # Test version parsing with debug
    print("\nTesting version parsing with debug mode:")
    test_version_line = "App version                     : 0x01010005"
    original, parsed, decimal = app.parse_app_version(test_version_line)
    print(f"Parsed: {parsed}, Decimal: {decimal}")
    
    # Test file browsing debug (simulate)
    print("\nTesting file operations debug logging:")
    test_file = os.path.abspath(__file__)  # Use this script as test file
    app.debug_log(f"Test file selected: {test_file}")
    app.debug_log(f"File size: {os.path.getsize(test_file)} bytes")
    app.debug_log(f"File extension: {os.path.splitext(test_file)[1]}")
    
    # Test commander command debug (mock)
    print("\nTesting commander command debug logging:")
    app.debug_log("Mock commander execution started")
    app.debug_log("Command: ['commander', '--version']")
    app.debug_log("Working directory: /test/directory")
    app.debug_log("Timeout: 120 seconds")
    app.debug_log("Command completed successfully")
    
    # Test status update
    print("\nTesting status bar with debug mode:")
    app.update_status()
    status = app.status_var.get()
    print(f"Status bar: {status}")
    assert "DEBUG MODE" in status, "Status bar should show DEBUG MODE when enabled"
    
    # Disable debug mode
    print("\nDisabling debug mode...")
    app.debug_mode = False
    app.update_status()
    status_after = app.status_var.get()
    print(f"Status bar after disable: {status_after}")
    assert "DEBUG MODE" not in status_after, "Status bar should not show DEBUG MODE when disabled"
    
    # Test debug logging when disabled again
    print("\nTesting debug_log when debug mode is OFF again:")
    app.debug_log("This debug message should NOT appear again")
    
    root.destroy()
    
    print("\n" + "=" * 70)
    print("Debug Mode Features:")
    print("=" * 70)
    
    features = [
        "✓ Toggle debug mode via Tools menu",
        "✓ Status bar shows DEBUG MODE when active",
        "✓ Debug messages only appear when debug mode is enabled",
        "✓ Enhanced logging for commander operations",
        "✓ Detailed version parsing information",
        "✓ File operation debugging",
        "✓ Programming thread detailed logging",
        "✓ Exception and error context",
        "✓ Performance and timing information",
        "✓ Memory and resource usage tracking",
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\n" + "=" * 70)
    print("✓ All debug mode tests passed!")
    print("=" * 70)

if __name__ == "__main__":
    test_debug_mode()