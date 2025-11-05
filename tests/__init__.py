# Tests for Zigbee Device Programmer
"""
Test suite for the Zigbee Device Programmer GUI application.

This package contains all test files for verifying the functionality of:
- Device mapping and JSON configuration
- GUI components and interactions
- Commander integration and programming logic
- Version parsing and verification
- Debug and erase functionality
- Button state management
- File selection and validation

To run all tests, execute the test files individually or use a test runner.
"""

__version__ = "1.0.0"
__author__ = "Zigbee Device Programmer Team"

# Test categories
UNIT_TESTS = [
    "test_zigbee_programmer.py",
    "test_device_mapping.py",
    "test_version_parsing.py",
    "test_filename_extraction.py",
    "test_commander_detection.py"
]

INTEGRATION_TESTS = [
    "test_integration.py",
    "test_actual_verification.py",
    "test_version_comparison.py",
    "test_exact_scenario.py"
]

GUI_TESTS = [
    "test_debug_mode.py",
    "test_erase_checkbox.py",
    "test_erase_validation.py",
    "test_program_button.py",
    "test_comprehensive_button.py",
    "test_device_mapping_json.py",
    "test_menu_functionality.py"
]

DEBUG_AND_DEMO = [
    "debug_colors.py",
    "demo_fix.py",
    "demo_version_comparison.py"
]

ALL_TESTS = UNIT_TESTS + INTEGRATION_TESTS + GUI_TESTS