#!/usr/bin/env python3
"""
File Operations Manager
Handles file selection, validation, and related operations for the Zigbee programmer
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox


class FileOperationsManager:
    """Manages file operations including selection, validation, and path handling"""
    
    def __init__(self, debug_callback=None, version_parser=None):
        self.debug_log = debug_callback or (lambda msg: None)
        self.version_parser = version_parser
        self._last_app_directory = None
        self._last_bootloader_directory = None
        
        # Remember last selected directories for better UX
        self._remember_directories = True
    
    def browse_application_file(self, current_path_var):
        """Browse and select application GBL file
        
        Args:
            current_path_var: tkinter StringVar to update with selected path
            
        Returns:
            tuple: (success: bool, selected_path: str or None, message: str)
        """
        try:
            # Determine initial directory
            initial_dir = self._get_initial_directory(
                current_path_var.get(), 
                self._last_app_directory
            )
            
            filename = filedialog.askopenfilename(
                title="Select Application GBL File",
                filetypes=[
                    ("GBL files", "*.gbl"),
                    ("All files", "*.*")
                ],
                initialdir=initial_dir
            )
            
            if filename:
                # Update the path variable
                current_path_var.set(filename)
                
                # Remember directory for next time
                if self._remember_directories:
                    self._last_app_directory = os.path.dirname(filename)
                
                # Validate the selected file
                validation_result = self._validate_gbl_file(filename, "application")
                
                if validation_result['is_valid']:
                    success_msg = f"Application file selected: {os.path.basename(filename)}"
                    if validation_result['version']:
                        success_msg += f" (Version: {validation_result['version']})"
                    
                    self.debug_log(f"Application file selected: {filename}")
                    self.debug_log(f"File size: {validation_result['size_mb']} MB")
                    
                    return True, filename, success_msg
                else:
                    error_msg = validation_result['error'] or "Invalid GBL file"
                    messagebox.showerror("Invalid File", error_msg)
                    return False, None, error_msg
            else:
                self.debug_log("Application file selection cancelled")
                return False, None, "File selection cancelled"
                
        except Exception as e:
            error_msg = f"Error selecting application file: {e}"
            self.debug_log(error_msg)
            messagebox.showerror("Error", error_msg)
            return False, None, error_msg
    
    def browse_bootloader_file(self, current_path_var):
        """Browse and select bootloader GBL file
        
        Args:
            current_path_var: tkinter StringVar to update with selected path
            
        Returns:
            tuple: (success: bool, selected_path: str or None, message: str)
        """
        try:
            # Determine initial directory
            initial_dir = self._get_initial_directory(
                current_path_var.get(), 
                self._last_bootloader_directory
            )
            
            filename = filedialog.askopenfilename(
                title="Select Bootloader GBL File",
                filetypes=[
                    ("GBL files", "*.gbl"),
                    ("All files", "*.*")
                ],
                initialdir=initial_dir
            )
            
            if filename:
                # Update the path variable
                current_path_var.set(filename)
                
                # Remember directory for next time
                if self._remember_directories:
                    self._last_bootloader_directory = os.path.dirname(filename)
                
                # Validate the selected file
                validation_result = self._validate_gbl_file(filename, "bootloader")
                
                if validation_result['is_valid']:
                    success_msg = f"Bootloader file selected: {os.path.basename(filename)}"
                    if validation_result['version']:
                        success_msg += f" (Version: {validation_result['version']})"
                    
                    self.debug_log(f"Bootloader file selected: {filename}")
                    self.debug_log(f"File size: {validation_result['size_mb']} MB")
                    
                    return True, filename, success_msg
                else:
                    error_msg = validation_result['error'] or "Invalid GBL file"
                    messagebox.showerror("Invalid File", error_msg)
                    return False, None, error_msg
            else:
                self.debug_log("Bootloader file selection cancelled")
                return False, None, "File selection cancelled"
                
        except Exception as e:
            error_msg = f"Error selecting bootloader file: {e}"
            self.debug_log(error_msg)
            messagebox.showerror("Error", error_msg)
            return False, None, error_msg
    
    def _get_initial_directory(self, current_path, last_directory):
        """Get the best initial directory for file dialog"""
        # If there's a current path, use its directory
        if current_path and os.path.exists(current_path):
            return os.path.dirname(current_path)
        
        # If we remember a last directory, use it
        if last_directory and os.path.exists(last_directory):
            return last_directory
        
        # Default to current working directory
        return os.getcwd()
    
    def _validate_gbl_file(self, file_path, file_type):
        """Validate that the selected file is a valid GBL file
        
        Args:
            file_path: Path to the file to validate
            file_type: Type of file ("application" or "bootloader")
            
        Returns:
            dict: Validation result with keys: is_valid, error, version, size_mb
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    'is_valid': False,
                    'error': f"File does not exist: {file_path}",
                    'version': None,
                    'size_mb': 0
                }
            
            # Check file extension
            if not file_path.lower().endswith('.gbl'):
                return {
                    'is_valid': False,
                    'error': f"File must have .gbl extension. Selected: {os.path.basename(file_path)}",
                    'version': None,
                    'size_mb': 0
                }
            
            # Check file size (should be reasonable)
            file_size = os.path.getsize(file_path)
            size_mb = round(file_size / (1024 * 1024), 2)
            
            # Basic size validation
            if file_size == 0:
                return {
                    'is_valid': False,
                    'error': "File is empty",
                    'version': None,
                    'size_mb': 0
                }
            
            if size_mb > 100:  # Arbitrary large size check
                return {
                    'is_valid': False,
                    'error': f"File seems too large ({size_mb} MB). Are you sure this is a firmware file?",
                    'version': None,
                    'size_mb': size_mb
                }
            
            # Try to extract version information if version parser is available
            version = None
            if self.version_parser:
                try:
                    version = self.version_parser.parse_version_from_filename(os.path.basename(file_path))
                except Exception as e:
                    self.debug_log(f"Could not parse version from filename: {e}")
            
            return {
                'is_valid': True,
                'error': None,
                'version': version,
                'size_mb': size_mb
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'error': f"Error validating file: {e}",
                'version': None,
                'size_mb': 0
            }
    
    def verify_application_version(self, device_display, app_file_path, device_manager=None):
        """Verify application version compatibility with selected device
        
        Args:
            device_display: Display name of selected device
            app_file_path: Path to application GBL file
            device_manager: DeviceMappingManager instance for device validation
            
        Returns:
            dict: Verification result with compatibility info
        """
        try:
            if not app_file_path or not os.path.exists(app_file_path):
                return {
                    'compatible': False,
                    'message': "No application file selected",
                    'warnings': []
                }
            
            filename = os.path.basename(app_file_path)
            warnings = []
            
            # Extract version information
            version_info = None
            if self.version_parser:
                version_info = self.version_parser.extract_firmware_info(app_file_path)
            
            # Check device compatibility if device manager available
            device_compatible = True
            if device_manager and version_info and version_info.get('device_hints'):
                # Try to match device hints with selected device
                actual_device = device_manager.get_actual_device_name(device_display)
                
                device_match_found = False
                for hint in version_info['device_hints']:
                    if hint.upper() in actual_device.upper() or actual_device.upper() in hint.upper():
                        device_match_found = True
                        break
                
                if not device_match_found:
                    device_compatible = False
                    warnings.append(
                        f"Device mismatch: Firmware appears to be for {', '.join(version_info['device_hints'])}, "
                        f"but selected device is {actual_device}"
                    )
            
            # Compile result
            if version_info and version_info.get('version'):
                message = f"Version {version_info['version']} detected"
                if version_info.get('device_hints'):
                    message += f" for {', '.join(version_info['device_hints'])}"
            else:
                message = "Version information could not be determined from filename"
                warnings.append("Could not parse version from filename - please verify compatibility manually")
            
            return {
                'compatible': device_compatible,
                'message': message,
                'warnings': warnings,
                'version_info': version_info
            }
            
        except Exception as e:
            error_msg = f"Error verifying application version: {e}"
            self.debug_log(error_msg)
            return {
                'compatible': False,
                'message': error_msg,
                'warnings': []
            }
    
    def get_file_display_info(self, file_path):
        """Get display information for a selected file
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: Formatted display information
        """
        if not file_path or not os.path.exists(file_path):
            return "No file selected"
        
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        size_mb = round(file_size / (1024 * 1024), 2)
        
        info_parts = [filename, f"{size_mb} MB"]
        
        # Add version info if available
        if self.version_parser:
            try:
                version = self.version_parser.parse_version_from_filename(filename)
                if version:
                    info_parts.insert(1, f"v{version}")
            except Exception:
                pass
        
        return " | ".join(info_parts)
    
    def clear_file_selection(self, path_var):
        """Clear a file selection
        
        Args:
            path_var: tkinter StringVar to clear
        """
        path_var.set("")
        self.debug_log("File selection cleared")
    
    def validate_required_files(self, app_file_path, bootloader_file_path=None, require_bootloader=False):
        """Validate that required files are selected and valid
        
        Args:
            app_file_path: Path to application file
            bootloader_file_path: Path to bootloader file (optional)
            require_bootloader: Whether bootloader is required
            
        Returns:
            tuple: (is_valid: bool, error_message: str or None)
        """
        # Check application file
        if not app_file_path:
            return False, "Application file is required"
        
        if not os.path.exists(app_file_path):
            return False, f"Application file not found: {app_file_path}"
        
        app_validation = self._validate_gbl_file(app_file_path, "application")
        if not app_validation['is_valid']:
            return False, f"Invalid application file: {app_validation['error']}"
        
        # Check bootloader file if provided or required
        if bootloader_file_path or require_bootloader:
            if not bootloader_file_path:
                return False, "Bootloader file is required"
            
            if not os.path.exists(bootloader_file_path):
                return False, f"Bootloader file not found: {bootloader_file_path}"
            
            bootloader_validation = self._validate_gbl_file(bootloader_file_path, "bootloader")
            if not bootloader_validation['is_valid']:
                return False, f"Invalid bootloader file: {bootloader_validation['error']}"
        
        return True, None