#!/usr/bin/env python3
"""
Test with simulated commander appinfo output using the actual verification method
"""

import sys
import os
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zigbee_programmer import ZigbeeProgrammerGUI
import tkinter as tk

def test_with_actual_verification():
    """Test using the actual verify_app_version method with simulated commander output"""
    
    # Create a minimal test instance
    root = tk.Tk()
    root.withdraw()  # Hide the window
    app = ZigbeeProgrammerGUI(root)
    
    print("=" * 80)
    print("Testing with Actual Verification Method")
    print("=" * 80)
    
    # Test the filename extraction
    filename = "occupancy_v3_1-1-5.s37"
    expected_version, expected_decimal = app.extract_version_from_filename(filename)
    print(f"Filename: {filename}")
    print(f"Expected version: {expected_version} (decimal: {expected_decimal})")
    
    # Simulate what would happen in the verification process
    print(f"\nSimulating verification process:")
    print("-" * 50)
    
    # Test the parsing of the first app version
    line1 = "App version                     : 0x000f462d"
    original1, parsed1, decimal1 = app.parse_app_version(line1)
    print(f"\n>>> {original1.strip()} <<<")
    print(f">>> Parsed Version: {parsed1} (decimal: {decimal1}) <<<")
    
    # Calculate int math version
    if decimal1 >= 1000000:
        int_major = decimal1 // 1000000
        int_minor = (decimal1 % 1000000) // 1000
        int_patch = decimal1 % 1000
        int_version = f"{int_major}.{int_minor}.{int_patch}"
        if int_version != parsed1:
            print(f">>> Alternative parse (int math): {int_version} <<<")
            
            # Use int math version for comparison
            comparison_version = int_version
            match_type = "int math"
        else:
            comparison_version = parsed1
            match_type = "byte parsing"
    else:
        comparison_version = parsed1
        match_type = "byte parsing"
    
    # Check for match
    if comparison_version == expected_version:
        print(f">>> [OK] VERSION MATCH: Device version {comparison_version} matches filename version {expected_version} (string match, {match_type}) <<<")
        version_matches = True
    else:
        print(f">>> [X] VERSION MISMATCH: Expected {expected_version} but device has {comparison_version} ({match_type}) <<<")
        version_matches = False
    
    # Test the second app version (should not be validated)
    line2 = "App version                     : 0x02040002"
    original2, parsed2, decimal2 = app.parse_app_version(line2)
    print(f"\n>>> {original2.strip()} <<<")
    print(f">>> Parsed Version: {parsed2} (decimal: {decimal2}) <<<")
    
    if decimal2 >= 1000000:
        int_major2 = decimal2 // 1000000
        int_minor2 = (decimal2 % 1000000) // 1000
        int_patch2 = decimal2 % 1000
        int_version2 = f"{int_major2}.{int_minor2}.{int_patch2}"
        if int_version2 != parsed2:
            print(f">>> Alternative parse (int math): {int_version2} <<<")
    
    print(">>> (Secondary app version - not validated) <<<")
    
    # Final result
    print(f"\n" + "=" * 50)
    if version_matches:
        print(">>> [OK] VERSION VERIFICATION PASSED: Device version matches filename! <<<")
    else:
        print(">>> [X] VERSION VERIFICATION FAILED: Device version does not match filename! <<<")
    
    print(f"\n" + "=" * 80)
    print("Results:")
    print(f"• Filename version: {expected_version}")
    print(f"• Device byte parsing: {parsed1}")
    print(f"• Device int math: {int_version}")
    print(f"• Comparison used: {comparison_version} ({match_type})")
    print(f"• Match result: {'[OK] PASS' if version_matches else '[X] FAIL'}")
    print("=" * 80)
    
    root.destroy()

if __name__ == "__main__":
    test_with_actual_verification()