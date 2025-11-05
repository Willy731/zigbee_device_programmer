#!/usr/bin/env python3
"""
Test script for filename version extraction
"""

import re
import os

def extract_version_from_filename(filename):
    """Extract version from filename using regex pattern
    
    Args:
        filename: The application filename (e.g., "msensor_2-1-7.ota" or "occupancy_v3_1-1-5.s37")
        
    Returns:
        tuple: (version_string, decimal_value) or (None, None) if not found
    """
    import re
    
    # Extract just the filename from the full path
    basename = os.path.basename(filename)
    
    # Multiple regex patterns to try in order
    patterns = [
        r'(\d{1,3}[-_]\d{1,3}[-_]\d{1,3})(?=[._])',  # Version followed by dot or underscore (e.g., "1-1-5.s37")
        r'_(\d{1,3}[-_]\d{1,3}[-_]\d{1,3})(?![-_]\d)', # Version after underscore, not followed by more digits
        r'(\d{1,3}[-_]\d{1,3}[-_]\d{1,3})',          # Any version pattern
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, basename)
        if matches:
            # Use the last match (most likely to be the actual version)
            version_string = matches[-1]
            
            # Normalize separators to hyphens for consistency
            normalized = version_string.replace('_', '-')
            
            # Split and convert to decimal using the same formula as JavaScript
            digits = normalized.split('-')
            decimal_value = (
                int(digits[0]) * 1000000 +
                int(digits[1]) * 1000 +
                int(digits[2])
            )
            
            # Convert to dot notation for display
            dot_version = f"{digits[0]}.{digits[1]}.{digits[2]}"
            
            return dot_version, decimal_value
    
    return None, None

def test_filename_extraction():
    """Test the filename version extraction with various formats"""
    test_cases = [
        "msensor_2-1-7.ota",
        "C:/workspaces/Final_Builds/occupancy_v3_1-1-5.s37",  # New underscore format
        "occupancy_v3_1-1-5.s37",  # New underscore format
        "application_1-0-3.hex",
        "/path/to/firmware_10-20-30.bin",
        "invalid_filename.ota",
        "app_1-2.ota",  # Should not match (only 2 parts)
        "test_999-888-777.s37",
        "prefix_0-0-1_suffix.hex",
        "v3_1-1-5.bin",  # Simplified underscore format
        "app_v2_5-6-7.ota",  # Mixed format
    ]
    
    print("=" * 60)
    print("Filename Version Extraction Test")
    print("=" * 60)
    
    for filename in test_cases:
        version, decimal = extract_version_from_filename(filename)
        print(f"\nFilename: {filename}")
        print(f"Extracted: {version if version else 'NO MATCH'}")
        print(f"Decimal:   {decimal if decimal else 'N/A'}")
        
        if version and decimal:
            # Verify the calculation
            parts = version.split('.')
            expected = int(parts[0]) * 1000000 + int(parts[1]) * 1000 + int(parts[2])
            print(f"Verify:    {expected} {'✓' if expected == decimal else '✗'}")
    
    print("\n" + "=" * 60)
    print("JavaScript comparison test:")
    
    # Test the exact example from the request
    filename = "msensor_2-1-7.ota"
    version, decimal = extract_version_from_filename(filename)
    expected_js = 2 * 1000000 + 1 * 1000 + 7  # JavaScript: 2001007
    
    print(f"Filename:        {filename}")
    print(f"Python result:   {version} → {decimal}")
    print(f"JavaScript calc: 2.1.7 → {expected_js}")
    print(f"Match:           {'✓' if decimal == expected_js else '✗'}")

if __name__ == "__main__":
    test_filename_extraction()