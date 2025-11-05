#!/usr/bin/env python3
"""
Test the exact scenario from the user's log
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_exact_scenario():
    """Test the exact scenario from the user's log"""
    
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from zigbee_programmer import ZigbeeProgrammerGUI
    import tkinter as tk
    
    # Create a minimal test instance
    root = tk.Tk()
    root.withdraw()  # Hide the window
    app = ZigbeeProgrammerGUI(root)
    
    print("=" * 80)
    print("Testing Exact Scenario from User Log")
    print("=" * 80)
    
    # Test filename extraction
    filename = "occupancy_v3_1-1-5.s37"
    expected_version, expected_decimal = app.extract_version_from_filename(filename)
    print(f"Filename: {filename}")
    print(f"Expected version: {expected_version} (decimal: {expected_decimal})")
    
    # Simulate the commander output with multiple app versions
    commander_output = """Some other info...
App version                     : 0x000f462d
More info...
App version                     : 0x02040002
Even more info..."""
    
    print(f"\nSimulated commander output:")
    print(commander_output)
    
    print(f"\nProcessing app versions:")
    print("-" * 50)
    
    # Process each app version line
    first_version_processed = False
    version_matches = False
    
    for line in commander_output.split('\n'):
        if 'App version' in line:
            original_line, parsed_version, decimal_value = app.parse_app_version(line)
            
            print(f"\n>>> {original_line.strip()} <<<")
            
            if parsed_version and decimal_value:
                print(f">>> Parsed Version: {parsed_version} (decimal: {decimal_value}) <<<")
                
                # Only validate the FIRST app version
                if not first_version_processed and expected_version:
                    first_version_processed = True
                    
                    if parsed_version == expected_version:
                        print(f">>> [OK] VERSION MATCH: Device version {parsed_version} matches filename version {expected_version} (string match) <<<")
                        version_matches = True
                    else:
                        print(f">>> [X] VERSION MISMATCH: Expected {expected_version} but device has {parsed_version} <<<")
                elif first_version_processed:
                    print(">>> (Secondary app version - not validated) <<<")
                
                # Show alternative parsing
                if decimal_value >= 1000000:
                    int_major = decimal_value // 1000000
                    int_minor = (decimal_value % 1000000) // 1000
                    int_patch = decimal_value % 1000
                    int_version = f"{int_major}.{int_minor}.{int_patch}"
                    if int_version != parsed_version:
                        print(f">>> Alternative parse (int math): {int_version} <<<")
            else:
                print(">>> Could not parse version number <<<")
    
    # Final verification result
    print(f"\n" + "=" * 50)
    if version_matches:
        print(">>> [OK] VERSION VERIFICATION PASSED: Device version matches filename! <<<")
    else:
        print(">>> [X] VERSION VERIFICATION FAILED: Device version does not match filename! <<<")
    
    print(f"\n" + "=" * 80)
    print("Expected behavior:")
    print("1. Only the FIRST app version (0x000f462d) should be validated")
    print("2. 0x000f462d should NOT match 1.1.5 from filename")
    print("3. Second app version (0x02040002) should be displayed but not validated")
    print("4. Final result should be VERIFICATION FAILED")
    print("=" * 80)
    
    root.destroy()

if __name__ == "__main__":
    test_exact_scenario()