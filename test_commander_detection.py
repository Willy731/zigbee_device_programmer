#!/usr/bin/env python3
"""
Test script for commander detection functionality
"""

import os
import platform
import shutil

def find_commander():
    """Find the Simplicity Commander executable"""
    print("Testing commander detection...")
    
    # First check if commander is in PATH
    commander_exe = "commander.exe" if platform.system() == "Windows" else "commander"
    
    commander_in_path = shutil.which(commander_exe)
    if commander_in_path:
        print(f"✓ Commander found in PATH: {commander_in_path}")
        return commander_in_path
    else:
        print("✗ Commander not found in PATH")
    
    # If not in PATH, check common installation locations
    if platform.system() == "Windows":
        common_paths = [
            r"C:\SiliconLabs\SimplicityStudio\v5\developer\adapter_packs\commander\Commander.exe",
            r"C:\SiliconLabs\SimplicityStudio\v4\developer\adapter_packs\commander\Commander.exe",
            r"C:\Program Files\Silicon Labs\Simplicity Studio\v5\developer\adapter_packs\commander\Commander.exe",
            r"C:\Program Files\Silicon Labs\Simplicity Studio\v4\developer\adapter_packs\commander\Commander.exe",
            r"C:\Program Files (x86)\Silicon Labs\Simplicity Studio\v5\developer\adapter_packs\commander\Commander.exe",
            r"C:\Program Files (x86)\Silicon Labs\Simplicity Studio\v4\developer\adapter_packs\commander\Commander.exe",
        ]
    else:
        # Linux/macOS paths
        common_paths = [
            "/opt/SimplicityStudio_v5/developer/adapter_packs/commander/Commander",
            "/opt/SimplicityStudio_v4/developer/adapter_packs/commander/Commander",
            "/Applications/Simplicity Studio.app/Contents/Eclipse/developer/adapter_packs/commander/Commander",
        ]
    
    print("\nChecking common installation locations:")
    for path in common_paths:
        if os.path.exists(path):
            print(f"✓ Found commander at: {path}")
            return path
        else:
            print(f"✗ Not found: {path}")
    
    print("\n❌ Commander not found in any standard location")
    return None

def main():
    print("=" * 60)
    print("Simplicity Commander Detection Test")
    print("=" * 60)
    
    commander_path = find_commander()
    
    print("\n" + "=" * 60)
    if commander_path:
        print(f"✅ SUCCESS: Commander detected at {commander_path}")
        print("\nRecommendations:")
        print("1. The application should work correctly")
        print("2. Test the commander by running: commander --version")
    else:
        print("❌ FAILED: Commander not detected")
        print("\nRecommendations:")
        print("1. Install Simplicity Studio from Silicon Labs")
        print("2. Add commander to your system PATH")
        print("3. Use the 'Set Commander Path' option in the GUI")
        print("4. Download commander standalone from Silicon Labs community")
    print("=" * 60)

if __name__ == "__main__":
    main()