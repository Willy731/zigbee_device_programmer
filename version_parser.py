#!/usr/bin/env python3
"""
Version Parser and Validator
Handles firmware version parsing and validation logic
"""

import re
import os


class VersionParser:
    """Handles parsing and validation of firmware versions"""
    
    def __init__(self, debug_callback=None):
        self.debug_log = debug_callback or (lambda msg: None)
    
    def parse_version_from_filename(self, filename):
        """Parse version information from GBL filename
        
        Supports various naming patterns:
        - xxx_v1.2.3_xxx.gbl
        - xxx_version_1.2.3_xxx.gbl
        - xxx_1.2.3_xxx.gbl
        - xxx-v1.2.3-xxx.gbl
        - xxx_1-2-3.gbl (dash format)
        """
        if not filename:
            return None
        
        base_name = os.path.basename(filename)
        
        # Common version patterns
        patterns = [
            r'[vV](\d+\.\d+\.\d+)',           # v1.2.3
            r'[vV](\d+\.\d+)',                # v1.2
            r'version[_\-](\d+\.\d+\.\d+)',   # version_1.2.3
            r'(\d+\.\d+\.\d+)',               # 1.2.3 (standalone)
            r'(\d+\.\d+)',                    # 1.2 (standalone)
            r'(\d+\-\d+\-\d+)',               # 1-2-3 (dash format)
            r'(\d+\-\d+)',                    # 1-2 (dash format)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, base_name, re.IGNORECASE)
            if match:
                version = match.group(1)
                # Convert dash format to dot format
                if '-' in version:
                    version = version.replace('-', '.')
                self.debug_log(f"Parsed version '{version}' from filename: {base_name}")
                return version
        
        self.debug_log(f"Could not parse version from filename: {base_name}")
        return None
    
    def validate_version_format(self, version_string):
        """Validate that version string follows semantic versioning
        
        Returns:
            tuple: (is_valid, normalized_version, error_message)
        """
        if not version_string:
            return False, None, "Version string is empty"
        
        # Remove any leading 'v' or 'V'
        clean_version = version_string.strip().lstrip('vV')
        
        # Check for basic semantic versioning pattern
        pattern = r'^(\d+)\.(\d+)(?:\.(\d+))?(?:[-+].*)?$'
        match = re.match(pattern, clean_version)
        
        if not match:
            return False, None, f"Invalid version format: {version_string}"
        
        major, minor, patch = match.groups()
        
        # If patch is not provided, default to 0
        if patch is None:
            patch = '0'
        
        normalized = f"{major}.{minor}.{patch}"
        
        return True, normalized, None
    
    def compare_versions(self, version1, version2):
        """Compare two version strings
        
        Returns:
            int: -1 if version1 < version2, 0 if equal, 1 if version1 > version2
        """
        def parse_version_parts(version):
            # Normalize and split version
            is_valid, normalized, _ = self.validate_version_format(version)
            if not is_valid:
                return [0, 0, 0]
            
            parts = normalized.split('.')
            return [int(part) for part in parts]
        
        parts1 = parse_version_parts(version1)
        parts2 = parse_version_parts(version2)
        
        # Compare each part
        for i in range(max(len(parts1), len(parts2))):
            p1 = parts1[i] if i < len(parts1) else 0
            p2 = parts2[i] if i < len(parts2) else 0
            
            if p1 < p2:
                return -1
            elif p1 > p2:
                return 1
        
        return 0
    
    def extract_firmware_info(self, gbl_path):
        """Extract comprehensive firmware information from GBL file path
        
        Returns:
            dict: Firmware information including version, device hints, etc.
        """
        if not gbl_path or not os.path.exists(gbl_path):
            return {
                'version': None,
                'filename': None,
                'device_hints': [],
                'size_mb': 0,
                'is_valid': False
            }
        
        filename = os.path.basename(gbl_path)
        file_size = os.path.getsize(gbl_path)
        size_mb = round(file_size / (1024 * 1024), 2)
        
        # Parse version
        version = self.parse_version_from_filename(filename)
        is_valid, normalized_version, _ = self.validate_version_format(version) if version else (False, None, None)
        
        # Extract device hints from filename
        device_hints = self._extract_device_hints(filename)
        
        return {
            'version': normalized_version if is_valid else version,
            'filename': filename,
            'device_hints': device_hints,
            'size_mb': size_mb,
            'is_valid': is_valid,
            'raw_version': version
        }
    
    def _extract_device_hints(self, filename):
        """Extract potential device names from filename"""
        device_hints = []
        
        # Common device patterns in filenames
        device_patterns = [
            r'(MGM\d+[A-Z]\d+[A-Z]+\d*[A-Z]*)',  # MGM220PC22HNA, MGM210PA22JIA
            r'(EFR\d+[A-Z]+\d+)',                 # EFR32BG22, EFR32MG21
            r'(BG\d+)',                           # BG22, BG21
            r'(MG\d+)',                           # MG22, MG21
        ]
        
        filename_upper = filename.upper()
        
        for pattern in device_patterns:
            matches = re.findall(pattern, filename_upper)
            device_hints.extend(matches)
        
        # Remove duplicates while preserving order
        unique_hints = []
        for hint in device_hints:
            if hint not in unique_hints:
                unique_hints.append(hint)
        
        return unique_hints
    
    def suggest_device_from_filename(self, filename, available_devices):
        """Suggest the best matching device from available devices based on filename
        
        Args:
            filename: The GBL filename
            available_devices: List of available device names
            
        Returns:
            str: Best matching device name or None
        """
        if not filename or not available_devices:
            return None
        
        device_hints = self._extract_device_hints(filename)
        
        if not device_hints:
            return None
        
        # Try to find exact matches first
        for hint in device_hints:
            for device in available_devices:
                if hint.upper() == device.upper():
                    self.debug_log(f"Found exact device match: {device} for hint: {hint}")
                    return device
        
        # Try partial matches
        for hint in device_hints:
            for device in available_devices:
                if hint.upper() in device.upper() or device.upper() in hint.upper():
                    self.debug_log(f"Found partial device match: {device} for hint: {hint}")
                    return device
        
        self.debug_log(f"No device match found for hints: {device_hints}")
        return None
    
    def get_version_info_display(self, gbl_path):
        """Get formatted version information for display
        
        Returns:
            str: Formatted version information
        """
        info = self.extract_firmware_info(gbl_path)
        
        if not info['is_valid']:
            return "No version information available"
        
        display_parts = [f"Version: {info['version']}"]
        
        if info['device_hints']:
            display_parts.append(f"Device hints: {', '.join(info['device_hints'])}")
        
        display_parts.append(f"Size: {info['size_mb']} MB")
        
        return " | ".join(display_parts)
    
    def extract_version_from_filename(self, filename):
        """Alias for parse_version_from_filename that returns tuple for backward compatibility"""
        version_string = self.parse_version_from_filename(filename)
        if version_string:
            decimal_value = self._version_string_to_decimal(version_string)
            return (version_string, decimal_value)
        return (None, None)
    
    def _version_string_to_decimal(self, version_string):
        """Convert version string like '2.1.7' to decimal equivalent like 0x02010007"""
        try:
            parts = version_string.split('.')
            if len(parts) >= 2:
                major = int(parts[0])
                minor = int(parts[1])
                patch = int(parts[2]) if len(parts) > 2 else 0
                
                # Pack into hex format: major.minor.0.patch -> 0xMMmmppPP
                decimal_value = (major << 24) | (minor << 16) | (patch)
                self.debug_log(f"Version {version_string} -> decimal {decimal_value} (0x{decimal_value:08x})")
                return decimal_value
        except (ValueError, IndexError) as e:
            self.debug_log(f"Error converting version {version_string} to decimal: {e}")
        return None