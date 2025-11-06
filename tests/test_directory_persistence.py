#!/usr/bin/env python3
"""
Test directory persistence functionality
"""

import os
import json
import tempfile
import tkinter as tk
from tkinter import StringVar
import pytest

# Import the modules to test
from device_manager import DeviceMappingManager
from file_operations import FileOperationsManager


class TestDirectoryPersistence:
    """Test cases for directory persistence functionality"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_settings_file = None
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window

    def teardown_method(self):
        """Clean up test fixtures"""
        if self.temp_settings_file and os.path.exists(self.temp_settings_file):
            try:
                os.unlink(self.temp_settings_file)
            except:
                pass
        
        try:
            self.root.destroy()
        except:
            pass

    def create_temp_settings(self, initial_settings=None):
        """Create a temporary settings file"""
        initial_settings = initial_settings or {"custom_mapping_path": None}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(initial_settings, temp_file)
            self.temp_settings_file = temp_file.name
        
        return self.temp_settings_file

    def test_initial_empty_settings(self):
        """Test behavior with empty settings"""
        settings_file = self.create_temp_settings()
        
        device_manager = DeviceMappingManager()
        device_manager.settings_file = settings_file
        
        file_ops = FileOperationsManager(settings_manager=device_manager)
        
        # Should have empty directories initially
        assert file_ops._last_app_directory is None
        assert file_ops._last_bootloader_directory is None
        
        # Directory settings should be empty
        dir_settings = device_manager.load_directory_settings()
        assert dir_settings == {}

    def test_directory_saving(self):
        """Test saving directory settings"""
        settings_file = self.create_temp_settings()
        
        device_manager = DeviceMappingManager()
        device_manager.settings_file = settings_file
        
        file_ops = FileOperationsManager(settings_manager=device_manager)
        
        # Set directories and save
        test_app_dir = "C:\\TestApp"
        test_boot_dir = "C:\\TestBootloader"
        
        file_ops._last_app_directory = test_app_dir
        file_ops._last_bootloader_directory = test_boot_dir
        file_ops._save_directory_settings()
        
        # Verify settings were saved to file
        with open(settings_file, 'r') as f:
            saved_settings = json.load(f)
        
        assert 'directory_settings' in saved_settings
        assert saved_settings['directory_settings']['last_app_directory'] == test_app_dir
        assert saved_settings['directory_settings']['last_bootloader_directory'] == test_boot_dir

    def test_directory_loading(self):
        """Test loading directory settings"""
        # Create settings with existing directories
        initial_settings = {
            "custom_mapping_path": None,
            "directory_settings": {
                "last_app_directory": "C:\\Apps",
                "last_bootloader_directory": "C:\\Boots"
            }
        }
        
        settings_file = self.create_temp_settings(initial_settings)
        
        device_manager = DeviceMappingManager()
        device_manager.settings_file = settings_file
        
        file_ops = FileOperationsManager(settings_manager=device_manager)
        
        # Should have loaded the directories
        assert file_ops._last_app_directory == "C:\\Apps"
        assert file_ops._last_bootloader_directory == "C:\\Boots"

    def test_directory_persistence_across_instances(self):
        """Test that directories persist across different instances"""
        settings_file = self.create_temp_settings()
        
        # First instance - set directories
        device_manager1 = DeviceMappingManager()
        device_manager1.settings_file = settings_file
        
        file_ops1 = FileOperationsManager(settings_manager=device_manager1)
        
        test_app_dir = "C:\\FirstApp"
        test_boot_dir = "C:\\FirstBoot"
        
        file_ops1._last_app_directory = test_app_dir
        file_ops1._last_bootloader_directory = test_boot_dir
        file_ops1._save_directory_settings()
        
        # Second instance - should load the same directories
        device_manager2 = DeviceMappingManager()
        device_manager2.settings_file = settings_file
        
        file_ops2 = FileOperationsManager(settings_manager=device_manager2)
        
        assert file_ops2._last_app_directory == test_app_dir
        assert file_ops2._last_bootloader_directory == test_boot_dir

    def test_get_initial_directory_logic(self):
        """Test the initial directory selection logic"""
        device_manager = DeviceMappingManager()
        file_ops = FileOperationsManager(settings_manager=device_manager)
        
        current_dir = os.getcwd()
        
        # Test with no previous directories
        initial_dir = file_ops._get_initial_directory("", None)
        assert initial_dir == current_dir
        
        # Test with current path
        current_file = os.path.abspath(__file__)
        expected_dir = os.path.dirname(current_file)
        initial_dir = file_ops._get_initial_directory(current_file, None)
        assert initial_dir == expected_dir
        
        # Test with last directory (non-existent)
        fake_dir = "C:\\NonExistent"
        initial_dir = file_ops._get_initial_directory("", fake_dir)
        assert initial_dir == current_dir  # Should fall back to current

    def test_directory_update_on_selection(self):
        """Test that directories are updated when new ones are selected"""
        settings_file = self.create_temp_settings()
        
        device_manager = DeviceMappingManager()
        device_manager.settings_file = settings_file
        
        file_ops = FileOperationsManager(settings_manager=device_manager)
        
        # Initially no directories
        assert file_ops._last_app_directory is None
        
        # Simulate directory change
        old_dir = "C:\\OldDir"
        new_dir = "C:\\NewDir"
        
        file_ops._last_app_directory = old_dir
        
        # Simulate new directory selection (like in browse methods)
        if new_dir != file_ops._last_app_directory:
            file_ops._last_app_directory = new_dir
            file_ops._save_directory_settings()
        
        # Verify the change was saved
        dir_settings = device_manager.load_directory_settings()
        assert dir_settings['last_app_directory'] == new_dir

    def test_separate_app_and_bootloader_directories(self):
        """Test that app and bootloader directories are stored separately"""
        settings_file = self.create_temp_settings()
        
        device_manager = DeviceMappingManager()
        device_manager.settings_file = settings_file
        
        file_ops = FileOperationsManager(settings_manager=device_manager)
        
        # Set different directories for each
        app_dir = "C:\\Applications"
        boot_dir = "C:\\Bootloaders"
        
        file_ops._last_app_directory = app_dir
        file_ops._last_bootloader_directory = boot_dir
        file_ops._save_directory_settings()
        
        # Create new instance to test loading
        device_manager2 = DeviceMappingManager()
        device_manager2.settings_file = settings_file
        
        file_ops2 = FileOperationsManager(settings_manager=device_manager2)
        
        # Should have different directories
        assert file_ops2._last_app_directory == app_dir
        assert file_ops2._last_bootloader_directory == boot_dir
        assert file_ops2._last_app_directory != file_ops2._last_bootloader_directory

    def test_settings_compatibility(self):
        """Test that new directory settings don't break existing settings"""
        # Create settings with existing custom mapping
        initial_settings = {
            "custom_mapping_path": "S:/custom/mapping.json"
        }
        
        settings_file = self.create_temp_settings(initial_settings)
        
        device_manager = DeviceMappingManager()
        device_manager.settings_file = settings_file
        
        file_ops = FileOperationsManager(settings_manager=device_manager)
        
        # Add directory settings
        file_ops._last_app_directory = "C:\\Test"
        file_ops._save_directory_settings()
        
        # Verify both old and new settings are preserved
        with open(settings_file, 'r') as f:
            saved_settings = json.load(f)
        
        assert saved_settings['custom_mapping_path'] == "S:/custom/mapping.json"
        assert 'directory_settings' in saved_settings
        assert saved_settings['directory_settings']['last_app_directory'] == "C:\\Test"


def test_directory_persistence():
    """Main test function for pytest compatibility"""
    # This function can be called by pytest directly
    test_suite = TestDirectoryPersistence()
    test_suite.setup_method()
    
    try:
        # Run a key test
        test_suite.test_directory_persistence_across_instances()
        
        # If we get here, the test passed
        assert True
        
    finally:
        test_suite.teardown_method()


if __name__ == "__main__":
    # Run tests directly
    test_class = TestDirectoryPersistence()
    
    test_methods = [
        test_class.test_initial_empty_settings,
        test_class.test_directory_saving,
        test_class.test_directory_loading,
        test_class.test_directory_persistence_across_instances,
        test_class.test_get_initial_directory_logic,
        test_class.test_directory_update_on_selection,
        test_class.test_separate_app_and_bootloader_directories,
        test_class.test_settings_compatibility,
    ]
    
    passed = 0
    total = len(test_methods)
    
    print("Running Directory Persistence Tests...")
    print("=" * 50)
    
    for i, test_method in enumerate(test_methods, 1):
        test_class.setup_method()
        try:
            test_method()
            print(f"✓ Test {i}/{total}: {test_method.__name__}")
            passed += 1
        except Exception as e:
            print(f"✗ Test {i}/{total}: {test_method.__name__} - {e}")
        finally:
            test_class.teardown_method()
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All directory persistence tests passed!")
    else:
        print("❌ Some tests failed!")
        exit(1)