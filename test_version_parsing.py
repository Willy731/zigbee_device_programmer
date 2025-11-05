#!/usr/bin/env python3
"""
Test script for version parsing functionality
"""

import re

def parse_app_version(version_line):
    """Parse application version from hex to decimal and format as version string
    
    Args:
        version_line: String containing the app version line from commander output
        
    Returns:
        tuple: (original_line, parsed_version, decimal_value) or (original_line, None, None) if parsing fails
    """
    
    # Look for hex values in the line (e.g., 0x01010005, 0x1010005, etc.)
    hex_pattern = r'0x([0-9a-fA-F]+)'
    hex_matches = re.findall(hex_pattern, version_line)
    
    if not hex_matches:
        # Try to find just hex digits after common prefixes
        hex_pattern = r'(?:version[:\s]+|v[:\s]*)?([0-9a-fA-F]{6,8})'
        hex_matches = re.findall(hex_pattern, version_line, re.IGNORECASE)
    
    if hex_matches:
        # Use the first hex value found
        hex_value = hex_matches[0]
        try:
            # Convert hex to decimal
            decimal_value = int(hex_value, 16)
            
            # Try to parse as byte-structured version first (e.g., 0x01010005 = v1.1.5)
            if len(hex_value) >= 6:  # At least 6 hex digits
                # Pad to 8 digits if needed
                padded_hex = hex_value.zfill(8)
                
                # Extract bytes: 0x01010005 -> 01, 01, 00, 05
                byte3 = int(padded_hex[0:2], 16)  # Major version
                byte2 = int(padded_hex[2:4], 16)  # Minor version  
                byte1 = int(padded_hex[4:6], 16)  # Usually 0
                byte0 = int(padded_hex[6:8], 16)  # Patch version
                
                # Format as version string
                if byte1 == 0:  # Standard case: major.minor.patch
                    parsed_version = f"{byte3}.{byte2}.{byte0}"
                else:  # Include all components
                    parsed_version = f"{byte3}.{byte2}.{byte1}.{byte0}"
            else:
                # Fallback: Parse decimal as version (assuming format: major*1000000 + minor*1000 + patch)
                if decimal_value >= 1000000:
                    major = decimal_value // 1000000
                    minor = (decimal_value % 1000000) // 1000
                    patch = decimal_value % 1000
                    parsed_version = f"{major}.{minor}.{patch}"
                else:
                    # Handle smaller values
                    if decimal_value >= 1000:
                        major = decimal_value // 1000
                        minor = decimal_value % 1000
                        parsed_version = f"{major}.{minor}"
                    else:
                        parsed_version = str(decimal_value)
            
            return version_line, parsed_version, decimal_value
        except ValueError:
            pass
    
    return version_line, None, None

def test_version_parsing():
    """Test the version parsing with various input formats"""
    test_cases = [
        "App version: 0x01010005",
        "App version: 0x1001005",  
        "Application version: 0x01010005",
        "App version: 1010005",
        "Version: 0x01000005",
        "App version 0x00010005",
        "Invalid line without version",
    ]
    
    print("=" * 60)
    print("Version Parsing Test")
    print("=" * 60)
    
    for test_case in test_cases:
        original, parsed, decimal = parse_app_version(test_case)
        print(f"\nInput:    {test_case}")
        print(f"Parsed:   {parsed if parsed else 'FAILED'}")
        print(f"Decimal:  {decimal if decimal else 'N/A'}")
        
        if parsed and decimal:
            # Verify the calculation
            if decimal >= 1000000:
                major = decimal // 1000000
                minor = (decimal % 1000000) // 1000
                patch = decimal % 1000
                verification = major * 1000000 + minor * 1000 + patch
                print(f"Verify:   {major}.{minor}.{patch} = {verification} ({'✓' if verification == decimal else '✗'})")
    
    print("\n" + "=" * 60)
    print("Manual calculation examples:")
    
    # Example calculations - testing byte parsing
    examples = [
        (0x01010005, "1.1.5"),
        (0x01000005, "1.0.5"), 
        (0x02003001, "2.0.1"),  # 0x02003001 -> bytes: 02, 00, 30, 01 -> 2.0.48.1 or 2.0.1 if middle byte ignored
        (0x1001005, "1.1.5"),   # 0x01001005 -> bytes: 01, 00, 10, 05 -> 1.0.16.5 or 1.0.5
    ]
    
    for hex_val, expected in examples:
        decimal = hex_val
        # Test byte parsing method
        padded_hex = f"{hex_val:08X}"
        byte3 = int(padded_hex[0:2], 16)  # Major
        byte2 = int(padded_hex[2:4], 16)  # Minor  
        byte1 = int(padded_hex[4:6], 16)  # Usually 0
        byte0 = int(padded_hex[6:8], 16)  # Patch
        
        if byte1 == 0:
            actual = f"{byte3}.{byte2}.{byte0}"
        else:
            actual = f"{byte3}.{byte2}.{byte1}.{byte0}"
            
        print(f"0x{hex_val:08X} ({decimal:8d}) → {actual} (expected: {expected}) {'✓' if actual == expected else '✗'}")
        print(f"    Bytes: {byte3:02X}.{byte2:02X}.{byte1:02X}.{byte0:02X}")
    
    # Test alternative parsing method (integer math)
    print(f"\nAlternative parsing (integer math):")
    test_decimal = 1001005  # The 7-digit number mentioned in the request
    major = test_decimal // 1000000
    minor = (test_decimal % 1000000) // 1000
    patch = test_decimal % 1000
    print(f"Decimal {test_decimal} → {major}.{minor}.{patch}")
    
    # Show the reverse calculation
    calculated = major * 1000000 + minor * 1000 + patch
    print(f"Reverse: {major}.{minor}.{patch} → {calculated}")

if __name__ == "__main__":
    test_version_parsing()