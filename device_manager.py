#!/usr/bin/env python3
"""
Device Mapping and Settings Manager
Handles device configuration mapping and application settings persistence
"""

import json
import os
from tkinter import messagebox


class DeviceMappingManager:
    """Manages device mapping configuration and settings"""
    
    def __init__(self, debug_callback=None):
        self.debug_log = debug_callback or (lambda msg: None)
        self.device_mapping = {}
        self.custom_mapping_path = None
        
        # Settings file for persistent configuration
        self.settings_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "zigbee_programmer_settings.json"
        )
        
        # Default device mapping as fallback
        self.default_mapping = {
            "MGM220PC22HNA": "MGM220PC22HNA",
            "MGM210PA22JIA": "MGM210PA22JIA",
            "MGM13P02F512GA": "MGM13P02F512GA",
        }
    
    def load_settings(self):
        """Load application settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.custom_mapping_path = settings.get('custom_mapping_path', None)
                    # Initialize directory settings if not present
                    if not hasattr(self, 'directory_settings'):
                        self.directory_settings = {}
                    self.directory_settings = settings.get('directory_settings', {})
                    self.debug_log(f"Settings loaded: custom_mapping_path = {self.custom_mapping_path}, directories = {self.directory_settings}")
            else:
                self.debug_log("No settings file found, using defaults")
                self.directory_settings = {}
        except Exception as e:
            self.debug_log(f"Error loading settings: {e}")
            self.custom_mapping_path = None
            self.directory_settings = {}
    
    def save_settings(self):
        """Save application settings to JSON file"""
        try:
            settings = {
                'custom_mapping_path': self.custom_mapping_path,
                'directory_settings': getattr(self, 'directory_settings', {})
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            self.debug_log(f"Settings saved: {settings}")
        except Exception as e:
            self.debug_log(f"Error saving settings: {e}")
    
    def load_device_mapping(self):
        """Load device mapping from JSON file"""
        # Load settings first to check for custom mapping path
        self.load_settings()
        
        # Try to load from custom mapping file first
        if self.custom_mapping_path and os.path.exists(self.custom_mapping_path):
            if self._load_mapping_from_file(self.custom_mapping_path, "custom"):
                return
        
        # Try to load from default mapping file
        default_mapping_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "device_mapping.json"
        )
        if os.path.exists(default_mapping_file):
            if self._load_mapping_from_file(default_mapping_file, "default"):
                return
        
        # Fallback to hardcoded mapping
        self.device_mapping = self.default_mapping.copy()
        self.debug_log("Using fallback hardcoded device mapping")
        self.debug_log(f"Loaded {len(self.device_mapping)} device mappings")
        
        # Create default mapping file if it doesn't exist
        self._create_default_mapping_file(default_mapping_file)
    
    def _load_mapping_from_file(self, file_path, file_type):
        """Load mapping from a specific file"""
        try:
            with open(file_path, 'r') as f:
                self.device_mapping = json.load(f)
            self.debug_log(f"Device mapping loaded from {file_type} file: {file_path}")
            self.debug_log(f"Loaded {len(self.device_mapping)} device mappings")
            return True
        except Exception as e:
            self.debug_log(f"Error loading {file_type} device mapping from {file_path}: {e}")
            if file_type == "custom":
                messagebox.showerror(
                    "Error", 
                    f"Failed to load custom device mapping:\n{e}\n\nFalling back to default mapping."
                )
            return False
    
    def _create_default_mapping_file(self, file_path):
        """Create default mapping file if it doesn't exist"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.default_mapping, f, indent=2)
            self.debug_log(f"Created default device mapping file: {file_path}")
        except Exception as e:
            self.debug_log(f"Error creating default device mapping file: {e}")
    
    def select_device_mapping_file(self, file_dialog_callback):
        """Allow user to select a custom device mapping JSON file"""
        filename = file_dialog_callback()
        
        if filename and os.path.exists(filename):
            try:
                # Test load the file to make sure it's valid
                with open(filename, 'r') as f:
                    test_mapping = json.load(f)
                
                # Validate that it's a dictionary
                if not isinstance(test_mapping, dict):
                    raise ValueError("Device mapping file must contain a JSON object (dictionary)")
                
                # Update the mapping
                self.custom_mapping_path = filename
                self.device_mapping = test_mapping
                
                # Save settings
                self.save_settings()
                
                success_msg = (
                    f"Device mapping loaded successfully!\n\n"
                    f"Loaded {len(self.device_mapping)} devices from:\n{filename}"
                )
                messagebox.showinfo("Success", success_msg)
                
                return True, f"Device mapping loaded from: {filename}"
                
            except Exception as e:
                error_msg = f"Failed to load device mapping file:\n\n{e}"
                messagebox.showerror("Error", error_msg)
                return False, f"ERROR: Failed to load device mapping from {filename}: {e}"
        else:
            self.debug_log("Device mapping file selection cancelled by user")
            return False, None
    
    def get_actual_device_name(self, display_name):
        """Get the actual chip name from the display name
        
        Args:
            display_name: The display name selected by the user
            
        Returns:
            str: The actual chip name for commander, or the display name if not found in mapping
        """
        return self.device_mapping.get(display_name, display_name)
    
    def get_device_display_names(self):
        """Get list of device display names for dropdown"""
        return list(self.device_mapping.keys())
    
    def get_mapping_info(self):
        """Get information about current mapping"""
        if self.custom_mapping_path:
            return f"Custom mapping: {os.path.basename(self.custom_mapping_path)}"
        else:
            return "device_mapping.json"
    
    def get_device_mapping(self):
        """Return the current device mapping dictionary"""
        return self.device_mapping.copy()
    
    def load_directory_settings(self):
        """Load directory settings from the settings file"""
        if not hasattr(self, 'directory_settings'):
            self.load_settings()  # This will initialize directory_settings
        return self.directory_settings.copy()
    
    def save_directory_settings(self, directory_settings):
        """Save directory settings to the settings file"""
        if not hasattr(self, 'directory_settings'):
            self.directory_settings = {}
        
        # Update the directory settings
        self.directory_settings.update(directory_settings)
        
        # Save all settings to file
        self.save_settings()