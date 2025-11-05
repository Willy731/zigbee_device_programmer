#!/usr/bin/env python3
"""
Integration test for the Zigbee programmer with version parsing
"""

# Test simulating commander appinfo output
def test_version_parsing_integration():
    """Test the integration with simulated commander output"""
    
    # Import the parsing function from the main module
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    
    from zigbee_programmer import ZigbeeProgrammerGUI
    import tkinter as tk
    
    # Create a minimal test instance
    root = tk.Tk()
    root.withdraw()  # Hide the window
    app = ZigbeeProgrammerGUI(root)
    
    # Test cases simulating real commander output
    test_outputs = [
        "App version: 0x01010005",
        "Application version: 0x01000003",
        "App version: 0x02000001", 
        "version: 1001005",  # Direct decimal
        "Some other line\nApp version: 0x01010005\nMore text",
    ]
    
    print("=" * 60)
    print("Integration Test - Version Parsing")
    print("=" * 60)
    
    for i, output in enumerate(test_outputs, 1):
        print(f"\nTest {i}: {repr(output)}")
        
        # Simulate the parsing logic
        for line in output.split('\n'):
            if 'App version' in line or 'version' in line.lower():
                original, parsed, decimal = app.parse_app_version(line)
                print(f"  Line: {line}")
                print(f"  Parsed: {parsed if parsed else 'FAILED'}")
                print(f"  Decimal: {decimal if decimal else 'N/A'}")
                
                if parsed and decimal:
                    # Test integer math comparison
                    if decimal >= 1000000:
                        int_major = decimal // 1000000
                        int_minor = (decimal % 1000000) // 1000
                        int_patch = decimal % 1000
                        int_version = f"{int_major}.{int_minor}.{int_patch}"
                        print(f"  Int math: {int_version}")
                        print(f"  Match: {'✓' if int_version == parsed else '✗'}")
    
    root.destroy()
    print("\n" + "=" * 60)
    print("Integration test completed!")

if __name__ == "__main__":
    test_version_parsing_integration()