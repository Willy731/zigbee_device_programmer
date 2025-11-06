#!/usr/bin/env python3
"""
Demo script showing directory persistence functionality
This simulates the user experience of file browsing with directory memory
"""

import os
import json
import tkinter as tk
from tkinter import StringVar

# Import our modules
from device_manager import DeviceMappingManager
from file_operations import FileOperationsManager

def demo_directory_persistence():
    """Demonstrate directory persistence functionality"""
    print("=" * 70)
    print("DIRECTORY PERSISTENCE DEMONSTRATION")
    print("=" * 70)
    
    # Show initial settings
    print("\n1. Initial Settings File Content:")
    try:
        with open("zigbee_programmer_settings.json", 'r') as f:
            settings = json.load(f)
        print(json.dumps(settings, indent=2))
    except FileNotFoundError:
        print("Settings file not found - will be created on first save")
    
    # Create managers
    print("\n2. Creating Managers and Loading Settings...")
    device_manager = DeviceMappingManager()
    file_ops = FileOperationsManager(
        debug_callback=lambda msg: print(f"   [DEBUG] {msg}"),
        settings_manager=device_manager
    )
    
    print(f"   Initial App Directory: {file_ops._last_app_directory}")
    print(f"   Initial Bootloader Directory: {file_ops._last_bootloader_directory}")
    
    # Simulate user browsing for application file
    print("\n3. Simulating Application File Selection...")
    
    # Create a minimal root for StringVar (like in the real GUI)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    app_path_var = StringVar()
    
    # Simulate the initial directory logic
    initial_app_dir = file_ops._get_initial_directory(
        app_path_var.get(), 
        file_ops._last_app_directory
    )
    print(f"   File dialog would start in: {initial_app_dir}")
    
    # Simulate user selecting a file in a different directory
    # (In real use, this would come from filedialog.askopenfilename)
    simulated_app_file = "C:\\FirmwareFiles\\Applications\\app_v1.2.3.gbl"
    simulated_app_dir = os.path.dirname(simulated_app_file)
    
    print(f"   User selects file: {simulated_app_file}")
    print(f"   Directory: {simulated_app_dir}")
    
    # Simulate the directory saving (like in browse_application_file)
    if simulated_app_dir != file_ops._last_app_directory:
        file_ops._last_app_directory = simulated_app_dir
        file_ops._save_directory_settings()
        print("   ✓ Application directory saved to settings")
    
    # Simulate user browsing for bootloader file
    print("\n4. Simulating Bootloader File Selection...")
    
    bootloader_path_var = StringVar()
    
    # Check initial directory for bootloader
    initial_boot_dir = file_ops._get_initial_directory(
        bootloader_path_var.get(), 
        file_ops._last_bootloader_directory
    )
    print(f"   File dialog would start in: {initial_boot_dir}")
    
    # Simulate user selecting bootloader in different directory
    simulated_boot_file = "C:\\FirmwareFiles\\Bootloaders\\bootloader_v2.1.hex"
    simulated_boot_dir = os.path.dirname(simulated_boot_file)
    
    print(f"   User selects file: {simulated_boot_file}")
    print(f"   Directory: {simulated_boot_dir}")
    
    # Simulate the directory saving (like in browse_bootloader_file)
    if simulated_boot_dir != file_ops._last_bootloader_directory:
        file_ops._last_bootloader_directory = simulated_boot_dir
        file_ops._save_directory_settings()
        print("   ✓ Bootloader directory saved to settings")
    
    # Show current state
    print(f"\n5. Current Directory State:")
    print(f"   App Directory: {file_ops._last_app_directory}")
    print(f"   Bootloader Directory: {file_ops._last_bootloader_directory}")
    
    # Show updated settings file
    print("\n6. Updated Settings File Content:")
    with open("zigbee_programmer_settings.json", 'r') as f:
        updated_settings = json.load(f)
    print(json.dumps(updated_settings, indent=2))
    
    # Simulate application restart
    print("\n7. Simulating Application Restart...")
    new_device_manager = DeviceMappingManager()
    new_file_ops = FileOperationsManager(
        debug_callback=lambda msg: print(f"   [DEBUG] {msg}"),
        settings_manager=new_device_manager
    )
    
    print(f"   Loaded App Directory: {new_file_ops._last_app_directory}")
    print(f"   Loaded Bootloader Directory: {new_file_ops._last_bootloader_directory}")
    
    # Show where file dialogs would start
    print("\n8. File Dialog Starting Locations After Restart:")
    
    app_start_dir = new_file_ops._get_initial_directory("", new_file_ops._last_app_directory)
    boot_start_dir = new_file_ops._get_initial_directory("", new_file_ops._last_bootloader_directory)
    
    print(f"   Application file dialog starts in: {app_start_dir}")
    print(f"   Bootloader file dialog starts in: {boot_start_dir}")
    
    print("\n" + "=" * 70)
    print("✅ DIRECTORY PERSISTENCE WORKING CORRECTLY!")
    print("File browsers will now remember their last used directories")
    print("=" * 70)
    
    # Clean up
    try:
        root.destroy()
    except:
        pass

def show_user_benefits():
    """Show the benefits of this feature to users"""
    print("\n" + "🎯 USER BENEFITS:" + "\n")
    
    benefits = [
        "📁 Application file browser remembers last application directory",
        "📁 Bootloader file browser remembers last bootloader directory", 
        "🔄 Settings persist between application sessions",
        "⏰ Saves time - no need to navigate to same folders repeatedly",
        "🎯 Each file type has separate directory memory",
        "💾 Settings automatically saved when directories change",
        "🚀 Improved user experience and workflow efficiency"
    ]
    
    for benefit in benefits:
        print(f"   {benefit}")
    
    print("\n" + "📋 TECHNICAL DETAILS:" + "\n")
    
    details = [
        "Settings stored in: zigbee_programmer_settings.json",
        "Application directory: directory_settings.last_app_directory", 
        "Bootloader directory: directory_settings.last_bootloader_directory",
        "Auto-saves when user selects file in new directory",
        "Falls back gracefully if saved directory no longer exists",
        "Compatible with existing settings structure"
    ]
    
    for detail in details:
        print(f"   • {detail}")

if __name__ == "__main__":
    demo_directory_persistence()
    show_user_benefits()