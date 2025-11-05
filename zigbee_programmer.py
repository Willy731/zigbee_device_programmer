#!/usr/bin/env python3
"""
Zigbee Device Programmer GUI
A GUI application to program Zigbee devices using Simplicity Commander
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import subprocess
import threading
import os
import tempfile
import shutil
import platform
import sys
import ctypes
import json


class ModernTheme:
    """Modern theme configuration for the application"""
    
    # Color palette - Modern dark theme
    DARK_BG = "#2b2b2b"
    DARKER_BG = "#1e1e1e"
    CARD_BG = "#3c3c3c"
    ACCENT = "#007acc"
    ACCENT_HOVER = "#005a9e"
    SUCCESS = "#4caf50"
    WARNING = "#ff9800"
    ERROR = "#f44336"
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    BORDER = "#555555"
    
    # Light theme alternative
    LIGHT_BG = "#ffffff"
    LIGHT_CARD_BG = "#f8f9fa"
    LIGHT_TEXT_PRIMARY = "#212529"
    LIGHT_TEXT_SECONDARY = "#6c757d"
    LIGHT_BORDER = "#dee2e6"
    
    @classmethod
    def configure_modern_style(cls, root, theme="dark"):
        """Configure modern ttk styles"""
        style = ttk.Style(root)
        
        if theme == "dark":
            # Configure dark theme
            style.theme_use('clam')
            
            # Configure colors
            style.configure(".", 
                          background=cls.DARK_BG,
                          foreground=cls.TEXT_PRIMARY,
                          bordercolor=cls.BORDER,
                          fieldbackground=cls.CARD_BG,
                          selectbackground=cls.ACCENT,
                          selectforeground=cls.TEXT_PRIMARY,
                          insertcolor=cls.TEXT_PRIMARY)
            
            # Modern button style
            style.configure("Modern.TButton",
                          background=cls.ACCENT,
                          foreground=cls.TEXT_PRIMARY,
                          borderwidth=0,
                          focuscolor="none",
                          relief="flat",
                          padding=(20, 10))
            
            style.map("Modern.TButton",
                     background=[('active', cls.ACCENT_HOVER),
                               ('pressed', cls.ACCENT_HOVER)])
            
            # Primary action button (larger, more prominent)
            style.configure("Primary.TButton",
                          background=cls.ACCENT,
                          foreground=cls.TEXT_PRIMARY,
                          borderwidth=0,
                          focuscolor="none",
                          relief="flat",
                          padding=(30, 15),
                          font=('Segoe UI', 10, 'bold'))
            
            style.map("Primary.TButton",
                     background=[('active', cls.ACCENT_HOVER),
                               ('pressed', cls.ACCENT_HOVER)])
            
            # Card frame style
            style.configure("Card.TFrame",
                          background=cls.CARD_BG,
                          borderwidth=1,
                          relief="solid",
                          bordercolor=cls.BORDER)
            
            # Modern entry style
            style.configure("Modern.TEntry",
                          fieldbackground=cls.CARD_BG,
                          borderwidth=1,
                          relief="solid",
                          bordercolor=cls.BORDER,
                          insertcolor=cls.TEXT_PRIMARY,
                          padding=(10, 8))
            
            style.map("Modern.TEntry",
                     bordercolor=[('focus', cls.ACCENT)])
            
            # Modern combobox style
            style.configure("Modern.TCombobox",
                          fieldbackground=cls.CARD_BG,
                          borderwidth=1,
                          relief="solid",
                          bordercolor=cls.BORDER,
                          arrowcolor=cls.TEXT_SECONDARY,
                          padding=(10, 8))
            
            style.map("Modern.TCombobox",
                     bordercolor=[('focus', cls.ACCENT)])
            
            # Modern label styles
            style.configure("Heading.TLabel",
                          background=cls.DARK_BG,
                          foreground=cls.TEXT_PRIMARY,
                          font=('Segoe UI', 12, 'bold'))
            
            style.configure("Subheading.TLabel",
                          background=cls.DARK_BG,
                          foreground=cls.TEXT_SECONDARY,
                          font=('Segoe UI', 9))
            
            # Modern checkbutton style
            style.configure("Modern.TCheckbutton",
                          background=cls.DARK_BG,
                          foreground=cls.TEXT_PRIMARY,
                          focuscolor="none",
                          font=('Segoe UI', 9))
            
            # Status styles
            style.configure("Success.TLabel",
                          background=cls.DARK_BG,
                          foreground=cls.SUCCESS,
                          font=('Segoe UI', 9))
            
            style.configure("Warning.TLabel",
                          background=cls.DARK_BG,
                          foreground=cls.WARNING,
                          font=('Segoe UI', 9))
            
            style.configure("Error.TLabel",
                          background=cls.DARK_BG,
                          foreground=cls.ERROR,
                          font=('Segoe UI', 9))
            
            # Configure root window
            root.configure(bg=cls.DARK_BG)
            
        else:  # light theme
            style.theme_use('clam')
            
            # Configure light theme colors
            style.configure(".", 
                          background=cls.LIGHT_BG,
                          foreground=cls.LIGHT_TEXT_PRIMARY,
                          bordercolor=cls.LIGHT_BORDER,
                          fieldbackground=cls.LIGHT_CARD_BG,
                          selectbackground=cls.ACCENT,
                          selectforeground=cls.TEXT_PRIMARY,
                          insertcolor=cls.LIGHT_TEXT_PRIMARY)
            
            # Modern button style (light)
            style.configure("Modern.TButton",
                          background=cls.ACCENT,
                          foreground=cls.TEXT_PRIMARY,
                          borderwidth=0,
                          focuscolor="none",
                          relief="flat",
                          padding=(20, 10))
            
            style.map("Modern.TButton",
                     background=[('active', cls.ACCENT_HOVER),
                               ('pressed', cls.ACCENT_HOVER)])
            
            # Primary action button (light)
            style.configure("Primary.TButton",
                          background=cls.ACCENT,
                          foreground=cls.TEXT_PRIMARY,
                          borderwidth=0,
                          focuscolor="none",
                          relief="flat",
                          padding=(30, 15),
                          font=('Segoe UI', 10, 'bold'))
            
            style.map("Primary.TButton",
                     background=[('active', cls.ACCENT_HOVER),
                               ('pressed', cls.ACCENT_HOVER)])
            
            # Modern combobox style (light)
            style.configure("Modern.TCombobox",
                          fieldbackground=cls.LIGHT_CARD_BG,
                          borderwidth=1,
                          relief="solid",
                          bordercolor=cls.LIGHT_BORDER,
                          arrowcolor=cls.LIGHT_TEXT_SECONDARY,
                          padding=(10, 8))
            
            style.map("Modern.TCombobox",
                     bordercolor=[('focus', cls.ACCENT)])
            
            # Modern checkbutton style (light)
            style.configure("Modern.TCheckbutton",
                          background=cls.LIGHT_BG,
                          foreground=cls.LIGHT_TEXT_PRIMARY,
                          focuscolor="none",
                          font=('Segoe UI', 9))
            
            # Configure root window
            root.configure(bg=cls.LIGHT_BG)
        
        return style


class ZigbeeProgrammerGUI:
    # Constants
    COMMANDER_TIMEOUT = 120  # Timeout for commander commands in seconds
    
    def __init__(self, root):
        self.root = root
        self.root.title("Zigbee Device Programmer")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Apply modern theme
        self.style = ModernTheme.configure_modern_style(root, theme="dark")
        self.current_theme = "dark"
        self.current_font_size = 10
        
        # Configure modern window icon and title styling
        if platform.system() == "Windows":
            try:
                # Set window icon if available
                icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
            except:
                pass
        
        # Variables
        self.device_var = tk.StringVar()
        self.app_file_var = tk.StringVar()
        self.bootloader_file_var = tk.StringVar()
        self.erase_before_flash = tk.BooleanVar()
        self.commander_path = None
        self.custom_mapping_path = None
        
        # Debug mode for verbose logging (must be set before loading device mapping)
        self.debug_mode = False
        
        # Settings file for persistent configuration
        self.settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zigbee_programmer_settings.json")
        
        # Load device mapping from JSON
        self.load_device_mapping()
        
        # Display names for the dropdown
        self.device_display_names = list(self.device_mapping.keys())
        
        # Find commander executable on startup
        self.find_commander()
        
        self.create_widgets()
        
    def find_commander(self):
        """Find the Simplicity Commander executable"""
        # First check if commander is in PATH
        commander_exe = "commander.exe" if platform.system() == "Windows" else "commander"
        
        if shutil.which(commander_exe):
            self.commander_path = commander_exe
            return True
        
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
        
        for path in common_paths:
            if os.path.exists(path):
                self.commander_path = path
                return True
        
        return False
    
    def get_actual_device_name(self, display_name):
        """Get the actual chip name from the display name
        
        Args:
            display_name: The display name selected by the user
            
        Returns:
            str: The actual chip name for commander, or the display name if not found in mapping
        """
        return self.device_mapping.get(display_name, display_name)
    
    def load_settings(self):
        """Load application settings from JSON file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.custom_mapping_path = settings.get('custom_mapping_path', None)
                    self.debug_log(f"Settings loaded: custom_mapping_path = {self.custom_mapping_path}")
            else:
                self.debug_log("No settings file found, using defaults")
        except Exception as e:
            self.debug_log(f"Error loading settings: {e}")
            self.custom_mapping_path = None
    
    def save_settings(self):
        """Save application settings to JSON file"""
        try:
            settings = {
                'custom_mapping_path': self.custom_mapping_path
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
        
        # Default device mapping as fallback
        default_mapping = {
            "MGM220PC22HNA": "MGM220PC22HNA",
            "MGM210PA22JIA": "MGM210PA22JIA",
            "MGM13P02F512GA": "MGM13P02F512GA",
        }
        
        # Try to load from custom mapping file first
        if self.custom_mapping_path and os.path.exists(self.custom_mapping_path):
            try:
                with open(self.custom_mapping_path, 'r') as f:
                    self.device_mapping = json.load(f)
                self.debug_log(f"Device mapping loaded from custom file: {self.custom_mapping_path}")
                self.debug_log(f"Loaded {len(self.device_mapping)} device mappings")
                return
            except Exception as e:
                self.debug_log(f"Error loading custom device mapping from {self.custom_mapping_path}: {e}")
                messagebox.showerror("Error", f"Failed to load custom device mapping:\n{e}\n\nFalling back to default mapping.")
        
        # Try to load from default mapping file
        default_mapping_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "device_mapping.json")
        if os.path.exists(default_mapping_file):
            try:
                with open(default_mapping_file, 'r') as f:
                    self.device_mapping = json.load(f)
                self.debug_log(f"Device mapping loaded from default file: {default_mapping_file}")
                self.debug_log(f"Loaded {len(self.device_mapping)} device mappings")
                return
            except Exception as e:
                self.debug_log(f"Error loading default device mapping file: {e}")
        
        # Fallback to hardcoded mapping
        self.device_mapping = default_mapping
        self.debug_log("Using fallback hardcoded device mapping")
        self.debug_log(f"Loaded {len(self.device_mapping)} device mappings")
        
        # Create default mapping file if it doesn't exist
        if not os.path.exists(default_mapping_file):
            try:
                with open(default_mapping_file, 'w') as f:
                    json.dump(default_mapping, f, indent=2)
                self.debug_log(f"Created default device mapping file: {default_mapping_file}")
            except Exception as e:
                self.debug_log(f"Error creating default device mapping file: {e}")
    
    def select_device_mapping_file(self):
        """Allow user to select a custom device mapping JSON file"""
        filename = filedialog.askopenfilename(
            title="Select Device Mapping JSON File",
            filetypes=[
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ],
            initialdir=os.path.dirname(os.path.abspath(__file__))
        )
        
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
                
                # Update the UI
                self.device_display_names = list(self.device_mapping.keys())
                self.refresh_device_dropdown()
                
                # Save settings
                self.save_settings()
                
                self.log(f"Device mapping loaded from: {filename}")
                self.debug_log(f"Loaded {len(self.device_mapping)} device mappings from custom file")
                messagebox.showinfo("Success", f"Device mapping loaded successfully!\n\nLoaded {len(self.device_mapping)} devices from:\n{filename}")
                
            except Exception as e:
                self.log(f"ERROR: Failed to load device mapping from {filename}: {e}")
                messagebox.showerror("Error", f"Failed to load device mapping file:\n\n{e}")
        else:
            self.debug_log("Device mapping file selection cancelled by user")
    
    def refresh_device_dropdown(self):
        """Refresh the device dropdown with current mapping"""
        if hasattr(self, 'device_combo'):
            # Update the combobox values
            self.device_combo.config(values=self.device_display_names)
            # Select first device if available
            if self.device_display_names:
                self.device_combo.current(0)
            else:
                self.device_var.set("")
    
    def check_commander_available(self):
        """Check if commander is available and show helpful error if not"""
        if self.commander_path is None:
            error_msg = (
                "Simplicity Commander not found!\n\n"
                "Please ensure Simplicity Commander is installed:\n"
                "1. Install Simplicity Studio from Silicon Labs\n"
                "2. Add Commander to your PATH, or\n"
                "3. Install it in one of these locations:\n"
                "   - C:\\SiliconLabs\\SimplicityStudio\\v5\\developer\\adapter_packs\\commander\\\n"
                "   - C:\\Program Files\\Silicon Labs\\Simplicity Studio\\v5\\developer\\adapter_packs\\commander\\\n\n"
                "You can also download Commander standalone from:\n"
                "https://community.silabs.com/s/article/simplicity-commander\n\n"
                "Use 'Tools > Set Commander Path' to manually specify the location."
            )
            messagebox.showerror("Commander Not Found", error_msg)
            self.log("ERROR: Simplicity Commander not found. Please install it and restart the application.")
            return False
        
        # Additional check: verify commander executable can run
        try:
            test_cmd = [self.commander_path, "--version"]
            result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                error_msg = (
                    f"Commander found at {self.commander_path} but failed to execute.\n\n"
                    "Possible issues:\n"
                    "1. Insufficient permissions - try running as administrator\n"
                    "2. Missing dependencies\n"
                    "3. Corrupted installation\n\n"
                    "Please reinstall Simplicity Commander or contact support."
                )
                messagebox.showerror("Commander Execution Error", error_msg)
                self.log(f"ERROR: Commander execution failed: {result.stderr}")
                return False
        except Exception as e:
            error_msg = (
                f"Commander found at {self.commander_path} but failed to execute.\n\n"
                f"Error: {str(e)}\n\n"
                "Try running the application as administrator or reinstall Commander."
            )
            messagebox.showerror("Commander Execution Error", error_msg)
            self.log(f"ERROR: Commander execution failed: {str(e)}")
            return False
        
        return True
        
    def create_widgets(self):
        # Create modern menu bar
        self.create_menu()
        
        # Main container with modern styling
        main_container = tk.Frame(self.root, bg=ModernTheme.DARK_BG)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header section (more compact)
        header_frame = tk.Frame(main_container, bg=ModernTheme.DARK_BG)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(header_frame, 
                              text="Zigbee Device Programmer", 
                              font=('Segoe UI', 16, 'bold'),
                              fg=ModernTheme.TEXT_PRIMARY,
                              bg=ModernTheme.DARK_BG)
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Modern programming interface for Zigbee devices",
                                 font=('Segoe UI', 9),
                                 fg=ModernTheme.TEXT_SECONDARY,
                                 bg=ModernTheme.DARK_BG)
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Main content area with cards
        content_frame = tk.Frame(main_container, bg=ModernTheme.DARK_BG)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for configuration (fixed width)
        left_panel = tk.Frame(content_frame, bg=ModernTheme.DARK_BG, width=450)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Device Configuration Card
        self.create_device_config_card(left_panel)
        
        # File Selection Card
        self.create_file_selection_card(left_panel)
        
        # Programming Options Card
        self.create_programming_options_card(left_panel)
        
        # Action Buttons Card
        self.create_action_buttons_card(left_panel)
        
        # Right panel for log output
        right_panel = tk.Frame(content_frame, bg=ModernTheme.DARK_BG)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Device Configuration Card
        self.create_device_config_card(left_panel)
        
        # File Selection Card
        self.create_file_selection_card(left_panel)
        
        # Programming Options Card
        self.create_programming_options_card(left_panel)
        
        # Action Buttons Card
        self.create_action_buttons_card(left_panel)
        
        # Right panel for log output
        right_panel = tk.Frame(content_frame, bg=ModernTheme.DARK_BG, width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_panel.pack_propagate(False)
        
        # Log Output Card
        self.create_log_output_card(right_panel)
        
        # Status bar at bottom
        self.create_modern_status_bar(main_container)
        
        # Initialize states
        self.update_status()
        self.update_program_button_state()
    
    def create_card_frame(self, parent, title):
        """Create a modern card-style frame with title"""
        # Get current theme colors
        bg_color = ModernTheme.DARK_BG if self.current_theme == "dark" else ModernTheme.LIGHT_BG
        card_bg = ModernTheme.CARD_BG if self.current_theme == "dark" else ModernTheme.LIGHT_CARD_BG
        text_color = ModernTheme.TEXT_PRIMARY if self.current_theme == "dark" else ModernTheme.LIGHT_TEXT_PRIMARY
        border_color = ModernTheme.BORDER if self.current_theme == "dark" else ModernTheme.LIGHT_BORDER
        
        # Card container (reduced spacing)
        card_container = tk.Frame(parent, bg=bg_color)
        card_container.pack(fill=tk.X, pady=(0, 10))
        
        # Card header (more compact)
        header_frame = tk.Frame(card_container, bg=card_bg, height=30)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text=title,
                              font=('Segoe UI', 10, 'bold'),
                              fg=text_color,
                              bg=card_bg)
        title_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        # Card content
        content_frame = tk.Frame(card_container, bg=card_bg, bd=1, relief='solid')
        content_frame.pack(fill=tk.X)
        content_frame.configure(highlightbackground=border_color, highlightcolor=border_color)
        
        return content_frame
    
    def create_device_config_card(self, parent):
        """Create device configuration card"""
        card_content = self.create_card_frame(parent, "Device Configuration")
        
        # Device selection with modern styling (reduced padding)
        device_frame = tk.Frame(card_content, bg=ModernTheme.CARD_BG)
        device_frame.pack(fill=tk.X, padx=15, pady=12)
        
        device_label = tk.Label(device_frame,
                               text="Target Device",
                               font=('Segoe UI', 9, 'bold'),
                               fg=ModernTheme.TEXT_PRIMARY,
                               bg=ModernTheme.CARD_BG)
        device_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.device_combo = ttk.Combobox(device_frame, 
                                        textvariable=self.device_var,
                                        values=self.device_display_names, 
                                        state="readonly",
                                        style="Modern.TCombobox",
                                        font=('Segoe UI', 10))
        self.device_combo.pack(fill=tk.X)
        if self.device_display_names:
            self.device_combo.current(0)
    
    def create_file_selection_card(self, parent):
        """Create file selection card"""
        card_content = self.create_card_frame(parent, "File Selection")
        
        # Application file selection (reduced padding)
        app_frame = tk.Frame(card_content, bg=ModernTheme.CARD_BG)
        app_frame.pack(fill=tk.X, padx=15, pady=(12, 8))
        
        app_label = tk.Label(app_frame,
                            text="Application File",
                            font=('Segoe UI', 9, 'bold'),
                            fg=ModernTheme.TEXT_PRIMARY,
                            bg=ModernTheme.CARD_BG)
        app_label.pack(anchor=tk.W, pady=(0, 4))
        
        app_input_frame = tk.Frame(app_frame, bg=ModernTheme.CARD_BG)
        app_input_frame.pack(fill=tk.X)
        
        self.app_entry = tk.Entry(app_input_frame,
                                 textvariable=self.app_file_var,
                                 font=('Segoe UI', 10),
                                 bg=ModernTheme.CARD_BG,
                                 fg=ModernTheme.TEXT_PRIMARY,
                                 insertbackground=ModernTheme.TEXT_PRIMARY,
                                 bd=1,
                                 relief='solid',
                                 highlightthickness=1,
                                 highlightcolor=ModernTheme.ACCENT,
                                 highlightbackground=ModernTheme.BORDER)
        self.app_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        app_browse_btn = ttk.Button(app_input_frame,
                                   text="Browse",
                                   command=self.browse_app_file,
                                   style="Modern.TButton")
        app_browse_btn.pack(side=tk.RIGHT)
        
        # Bootloader file selection (reduced padding)
        boot_frame = tk.Frame(card_content, bg=ModernTheme.CARD_BG)
        boot_frame.pack(fill=tk.X, padx=15, pady=(8, 12))
        
        boot_label_frame = tk.Frame(boot_frame, bg=ModernTheme.CARD_BG)
        boot_label_frame.pack(fill=tk.X, pady=(0, 4))
        
        boot_label = tk.Label(boot_label_frame,
                             text="Bootloader File",
                             font=('Segoe UI', 9, 'bold'),
                             fg=ModernTheme.TEXT_PRIMARY,
                             bg=ModernTheme.CARD_BG)
        boot_label.pack(side=tk.LEFT)
        
        self.bootloader_optional_label = tk.Label(boot_label_frame,
                                                  text="(Optional)",
                                                  font=('Segoe UI', 8, 'italic'),
                                                  fg=ModernTheme.TEXT_SECONDARY,
                                                  bg=ModernTheme.CARD_BG)
        self.bootloader_optional_label.pack(side=tk.LEFT, padx=(5, 0))
        
        boot_input_frame = tk.Frame(boot_frame, bg=ModernTheme.CARD_BG)
        boot_input_frame.pack(fill=tk.X)
        
        self.boot_entry = tk.Entry(boot_input_frame,
                                  textvariable=self.bootloader_file_var,
                                  font=('Segoe UI', 10),
                                  bg=ModernTheme.CARD_BG,
                                  fg=ModernTheme.TEXT_PRIMARY,
                                  insertbackground=ModernTheme.TEXT_PRIMARY,
                                  bd=1,
                                  relief='solid',
                                  highlightthickness=1,
                                  highlightcolor=ModernTheme.ACCENT,
                                  highlightbackground=ModernTheme.BORDER)
        self.boot_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        boot_browse_btn = ttk.Button(boot_input_frame,
                                    text="Browse",
                                    command=self.browse_bootloader_file,
                                    style="Modern.TButton")
        boot_browse_btn.pack(side=tk.RIGHT)
    
    def create_programming_options_card(self, parent):
        """Create programming options card"""
        card_content = self.create_card_frame(parent, "Programming Options")
        
        options_frame = tk.Frame(card_content, bg=ModernTheme.CARD_BG)
        options_frame.pack(fill=tk.X, padx=15, pady=12)
        
        self.erase_checkbox = ttk.Checkbutton(options_frame,
                                             text="Erase Before Flash",
                                             variable=self.erase_before_flash,
                                             command=self.on_erase_checkbox_changed,
                                             style="Modern.TCheckbutton")
        self.erase_checkbox.pack(anchor=tk.W)
        
        erase_info = tk.Label(options_frame,
                             text="Performs a full device erase before programming",
                             font=('Segoe UI', 8),
                             fg=ModernTheme.TEXT_SECONDARY,
                             bg=ModernTheme.CARD_BG)
        erase_info.pack(anchor=tk.W, pady=(3, 0))
    
    def create_action_buttons_card(self, parent):
        """Create action buttons card"""
        card_content = self.create_card_frame(parent, "Actions")
        
        button_frame = tk.Frame(card_content, bg=ModernTheme.CARD_BG)
        button_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # Primary program button
        self.program_button = ttk.Button(button_frame,
                                        text="Program Device",
                                        command=self.program_device,
                                        style="Primary.TButton")
        self.program_button.pack(fill=tk.X, pady=(0, 8))
        
        # Secondary action buttons
        secondary_frame = tk.Frame(button_frame, bg=ModernTheme.CARD_BG)
        secondary_frame.pack(fill=tk.X)
        
        check_btn = ttk.Button(secondary_frame,
                              text="Check Commander",
                              command=self.check_commander_status,
                              style="Modern.TButton")
        check_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        clear_btn = ttk.Button(secondary_frame,
                              text="Clear Log",
                              command=self.clear_log,
                              style="Modern.TButton")
        clear_btn.pack(side=tk.LEFT)
    
    def create_log_output_card(self, parent):
        """Create log output card"""
        card_content = self.create_card_frame(parent, "Log Output")
        
        log_frame = tk.Frame(card_content, bg=ModernTheme.CARD_BG)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        # Create custom styled text widget
        self.log_text = tk.Text(log_frame,
                               wrap=tk.WORD,
                               font=('Consolas', 9),
                               bg=ModernTheme.DARKER_BG,
                               fg=ModernTheme.TEXT_PRIMARY,
                               insertbackground=ModernTheme.TEXT_PRIMARY,
                               selectbackground=ModernTheme.ACCENT,
                               selectforeground=ModernTheme.TEXT_PRIMARY,
                               bd=1,
                               relief='solid',
                               highlightthickness=0)
        
        # Create custom scrollbar
        scrollbar = tk.Scrollbar(log_frame,
                                bg=ModernTheme.CARD_BG,
                                troughcolor=ModernTheme.DARKER_BG,
                                activebackground=ModernTheme.ACCENT,
                                highlightthickness=0)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # Configure text tags for colored output
        self.log_text.tag_configure("success", foreground=ModernTheme.SUCCESS)
        self.log_text.tag_configure("warning", foreground=ModernTheme.WARNING)
        self.log_text.tag_configure("error", foreground=ModernTheme.ERROR)
        self.log_text.tag_configure("info", foreground=ModernTheme.ACCENT)
    
    def create_modern_status_bar(self, parent):
        """Create modern status bar"""
        status_frame = tk.Frame(parent, bg=ModernTheme.DARKER_BG, height=25)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(status_frame,
                                    textvariable=self.status_var,
                                    font=('Segoe UI', 8),
                                    fg=ModernTheme.TEXT_SECONDARY,
                                    bg=ModernTheme.DARKER_BG,
                                    anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=12, pady=4)
        
    def create_menu(self):
        """Create the application menu with modern styling"""
        menubar = tk.Menu(self.root,
                         bg=ModernTheme.CARD_BG,
                         fg=ModernTheme.TEXT_PRIMARY,
                         activebackground=ModernTheme.ACCENT,
                         activeforeground=ModernTheme.TEXT_PRIMARY,
                         borderwidth=0)
        self.root.config(menu=menubar)
        
        # View menu for theme options
        view_menu = tk.Menu(menubar, tearoff=0,
                           bg=ModernTheme.CARD_BG,
                           fg=ModernTheme.TEXT_PRIMARY,
                           activebackground=ModernTheme.ACCENT,
                           activeforeground=ModernTheme.TEXT_PRIMARY,
                           borderwidth=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark/Light Theme", command=self.toggle_theme)
        view_menu.add_separator()
        view_menu.add_command(label="Increase Font Size", command=self.increase_font_size)
        view_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size)
        view_menu.add_command(label="Reset Font Size", command=self.reset_font_size)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0,
                            bg=ModernTheme.CARD_BG,
                            fg=ModernTheme.TEXT_PRIMARY,
                            activebackground=ModernTheme.ACCENT,
                            activeforeground=ModernTheme.TEXT_PRIMARY,
                            borderwidth=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Check Commander Status", command=self.check_commander_status)
        tools_menu.add_command(label="Set Commander Path...", command=self.set_commander_path)
        tools_menu.add_command(label="Test Device Connection", command=self.test_device_connection)
        tools_menu.add_separator()
        tools_menu.add_command(label="Select Device Mapping File...", command=self.select_device_mapping_file)
        tools_menu.add_separator()
        tools_menu.add_command(label="Toggle Debug Mode", command=self.toggle_debug_mode)
        tools_menu.add_separator()
        tools_menu.add_command(label="Refresh Commander", command=self.refresh_commander)
        if platform.system() == "Windows":
            tools_menu.add_separator()
            tools_menu.add_command(label="Restart as Administrator", command=self.restart_as_admin)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0,
                           bg=ModernTheme.CARD_BG,
                           fg=ModernTheme.TEXT_PRIMARY,
                           activebackground=ModernTheme.ACCENT,
                           activeforeground=ModernTheme.TEXT_PRIMARY,
                           borderwidth=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About Commander", command=self.show_commander_help)
        help_menu.add_separator()
        help_menu.add_command(label="About Application", command=self.show_about)
    
    def set_commander_path(self):
        """Allow user to manually set the commander path"""
        filename = filedialog.askopenfilename(
            title="Select Simplicity Commander Executable",
            filetypes=[
                ("Executable Files", "*.exe" if platform.system() == "Windows" else "*"),
                ("All Files", "*.*")
            ]
        )
        if filename and os.path.exists(filename):
            self.commander_path = filename
            self.log(f"Commander path set to: {filename}")
            self.update_status()
            messagebox.showinfo("Success", f"Commander path updated to:\n{filename}")
    
    def refresh_commander(self):
        """Re-search for commander"""
        self.log("\n=== Searching for Simplicity Commander ===")
        if self.find_commander():
            self.log(f"Commander found at: {self.commander_path}")
            messagebox.showinfo("Success", f"Commander found at:\n{self.commander_path}")
        else:
            self.log("Commander not found in standard locations")
            messagebox.showwarning("Not Found", "Commander not found in standard locations.\nPlease use 'Tools > Set Commander Path' to set it manually.")
        self.update_status()
    
    def test_device_connection(self):
        """Test device connection and permissions"""
        if not self.check_commander_available():
            return
        
        device_display = self.device_var.get()
        if not device_display:
            messagebox.showwarning("No Device Selected", "Please select a device before testing connection.")
            return
        
        device = self.get_actual_device_name(device_display)
        
        self.log("\n=== Testing Device Connection ===")
        self.log(f"Testing connection to device: {device_display} ({device})")
        
        # Test with device list command
        list_cmd = [self.commander_path, "adapter", "list"]
        success, stdout, stderr = self.run_commander_command(list_cmd)
        
        if success:
            self.log("Device adapters found:")
            if "J-Link" in stdout or "adapter" in stdout.lower():
                self.log("✓ J-Link adapter detected")
                
                # Test device-specific connection
                probe_cmd = [self.commander_path, "adapter", "probe", "--device", device]
                success2, stdout2, stderr2 = self.run_commander_command(probe_cmd)
                
                if success2:
                    self.log(f"✓ Successfully connected to {device_display} ({device})")
                    messagebox.showinfo("Success", f"Device {device_display} is connected and accessible!")
                else:
                    error_msg = (
                        f"Found adapters but failed to connect to {device_display} ({device}).\n\n"
                        "Possible issues:\n"
                        "1. Device not connected or powered\n"
                        "2. Wrong device type selected\n"
                        "3. Device in use by another application\n"
                        "4. USB driver issues\n\n"
                        "Try:\n"
                        "- Disconnect and reconnect the device\n"
                        "- Close other applications using the device\n"
                        "- Run as administrator\n"
                        "- Check device drivers"
                    )
                    messagebox.showerror("Connection Failed", error_msg)
            else:
                error_msg = (
                    "No compatible adapters found.\n\n"
                    "Please ensure:\n"
                    "1. J-Link device is connected\n"
                    "2. USB drivers are installed\n"
                    "3. Device is powered on\n"
                    "4. Run as administrator if needed"
                )
                messagebox.showerror("No Adapters", error_msg)
        else:
            error_msg = (
                "Failed to list adapters.\n\n"
                "This usually indicates:\n"
                "1. Permission issues - try running as administrator\n"
                "2. Driver problems\n"
                "3. Commander installation issues\n\n"
                f"Error details:\n{stderr}"
            )
            messagebox.showerror("Adapter List Failed", error_msg)
    
    def restart_as_admin(self):
        """Restart the application as administrator (Windows only)"""
        if platform.system() != "Windows":
            messagebox.showinfo("Not Available", "This feature is only available on Windows.")
            return
        
        try:
            # Check if already running as admin
            if ctypes.windll.shell32.IsUserAnAdmin():
                messagebox.showinfo("Already Administrator", "Application is already running as administrator.")
                return
            
            if messagebox.askyesno("Restart as Administrator", 
                                 "This will restart the application with administrator privileges.\n\nContinue?"):
                # Get the current script path
                script_path = os.path.abspath(sys.argv[0])
                
                # Restart with admin privileges
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f'"{script_path}"', None, 1
                )
                
                # Close current instance
                self.root.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restart as administrator: {str(e)}")
    
    def is_admin(self):
        """Check if running as administrator (Windows only)"""
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        return True  # Assume admin on non-Windows
    
    def show_commander_help(self):
        """Show help information about commander setup"""
        help_text = """Simplicity Commander Setup Help

To use this application, you need Simplicity Commander installed:

1. Download and install Simplicity Studio from Silicon Labs:
   https://www.silabs.com/developers/simplicity-studio

2. Alternatively, download Commander standalone:
   https://community.silabs.com/s/article/simplicity-commander

3. Common installation paths:
   • C:\\SiliconLabs\\SimplicityStudio\\v5\\developer\\adapter_packs\\commander\\
   • C:\\Program Files\\Silicon Labs\\Simplicity Studio\\v5\\developer\\adapter_packs\\commander\\

4. Add Commander to your system PATH, or use 'Tools > Set Commander Path' 
   to manually specify the location.

5. Ensure your J-Link drivers are installed and the device is connected.

DEVICE MAPPING:
Device names are loaded from JSON files for easy customization:
• Default mapping is stored in 'device_mapping.json'
• Use 'Tools > Select Device Mapping File...' to load custom mappings
• Custom mapping file path is saved and restored on restart
• JSON format: {"Display Name": "Actual Chip Name"}
• Status bar shows which mapping file is currently active

DEBUG MODE:
Use 'Tools > Toggle Debug Mode' to enable verbose logging:
• Shows detailed command execution information
• Displays file operation details and validation steps
• Provides enhanced version parsing information
• Includes exception context and timing information
• Status bar shows "DEBUG MODE" when active

PERMISSION ISSUES:
If you get "access denied" or "permission" errors:
• Run this application as Administrator
• Ensure no other applications are using the device
• Check that J-Link drivers are properly installed
• Try disconnecting and reconnecting the device

TROUBLESHOOTING:
• Use 'Tools > Check Commander Status' to verify installation
• Use 'Tools > Test Device Connection' to check device connectivity
• Enable 'Tools > Toggle Debug Mode' for detailed logging
• Check the log output for detailed error messages

For support, visit: https://community.silabs.com/"""
        
        messagebox.showinfo("Commander Setup Help", help_text)
        
    def check_commander_status(self):
        """Check and display commander status"""
        self.log("\n=== Checking Simplicity Commander Status ===")
        if self.commander_path:
            self.log(f"Commander found at: {self.commander_path}")
            
            # Test commander by running version command
            try:
                version_cmd = [self.commander_path, "--version"]
                result = subprocess.run(version_cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.log("Commander is working correctly!")
                    if result.stdout:
                        self.log(f"Version info: {result.stdout.strip()}")
                else:
                    self.log("Commander found but may not be working correctly")
                    if result.stderr:
                        self.log(f"Error: {result.stderr}")
            except Exception as e:
                self.log(f"Error testing commander: {e}")
        else:
            self.log("Commander not found!")
            self.check_commander_available()
        
        self.update_status()
    
    def toggle_debug_mode(self):
        """Toggle debug mode for verbose logging"""
        self.debug_mode = not self.debug_mode
        
        if self.debug_mode:
            self.log("=" * 60)
            self.log("DEBUG MODE ENABLED")
            self.log("Verbose logging is now active")
            self.log("=" * 60)
            messagebox.showinfo("Debug Mode", "Debug mode enabled!\n\nVerbose logging is now active. You will see more detailed information in the log output.")
        else:
            self.log("=" * 60)
            self.log("DEBUG MODE DISABLED")
            self.log("Verbose logging is now inactive")
            self.log("=" * 60)
            messagebox.showinfo("Debug Mode", "Debug mode disabled!\n\nVerbose logging is now inactive.")
        
        self.update_status()
    
    def debug_log(self, message):
        """Add debug message to log window (only if debug mode is enabled)
        
        Args:
            message: Debug message to log
        """
        if self.debug_mode:
            self.log(f"[DEBUG] {message}")
    
    def update_status(self):
        """Update the status bar"""
        status_parts = []
        
        if self.commander_path:
            status_parts.append("Commander available")
        else:
            status_parts.append("Commander NOT FOUND")
        
        # Add device mapping info
        if self.custom_mapping_path:
            mapping_name = os.path.basename(self.custom_mapping_path)
            status_parts.append(f"Custom mapping: {mapping_name}")
        else:
            status_parts.append("Default mapping")
        
        if platform.system() == "Windows":
            if self.is_admin():
                status_parts.append("Running as Administrator")
            else:
                status_parts.append("Running as User")
        
        if self.debug_mode:
            status_parts.append("DEBUG MODE")
        
        self.status_var.set(" | ".join(status_parts))
        
    def browse_app_file(self):
        filename = filedialog.askopenfilename(
            title="Select Application File",
            filetypes=[
                ("Binary Files", "*.bin *.hex *.s37 *.gbl"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.app_file_var.set(filename)
            self.log(f"Selected application file: {filename}")
            self.debug_log(f"Application file selected - path: {filename}")
            self.debug_log(f"File size: {os.path.getsize(filename) if os.path.exists(filename) else 'File not found'} bytes")
            self.debug_log(f"File extension: {os.path.splitext(filename)[1]}")
        else:
            self.debug_log("Application file selection cancelled by user")
        
        # Update program button state
        self.update_program_button_state()
    
    def browse_bootloader_file(self):
        filename = filedialog.askopenfilename(
            title="Select Bootloader File",
            filetypes=[
                ("Binary Files", "*.bin *.hex *.s37"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.bootloader_file_var.set(filename)
            self.log(f"Selected bootloader file: {filename}")
            self.debug_log(f"Bootloader file selected - path: {filename}")
            self.debug_log(f"File size: {os.path.getsize(filename) if os.path.exists(filename) else 'File not found'} bytes")
            self.debug_log(f"File extension: {os.path.splitext(filename)[1]}")
        else:
            self.debug_log("Bootloader file selection cancelled by user")
        
        # Update program button state
        self.update_program_button_state()
    
    def on_erase_checkbox_changed(self):
        """Handle the erase before flash checkbox state change"""
        if self.erase_before_flash.get():
            # When erase is checked, bootloader becomes mandatory
            self.bootloader_optional_label.config(text="(Required for Erase)", fg=ModernTheme.ERROR)
            self.debug_log("Erase before flash enabled - bootloader is now required")
        else:
            # When erase is unchecked, bootloader is optional again
            self.bootloader_optional_label.config(text="(Optional)", fg=ModernTheme.TEXT_SECONDARY)
            self.debug_log("Erase before flash disabled - bootloader is now optional")
        
        # Update program button state
        self.update_program_button_state()
    
    def update_program_button_state(self):
        """Enable/disable the Program Device button based on current selections"""
        app_file = self.app_file_var.get().strip()
        bootloader_file = self.bootloader_file_var.get().strip()
        erase_enabled = self.erase_before_flash.get()
        
        # Check if application file is selected
        app_file_valid = bool(app_file and os.path.exists(app_file))
        
        # Check if bootloader is required and valid
        if erase_enabled:
            # When erase is enabled, bootloader is mandatory
            bootloader_valid = bool(bootloader_file and os.path.exists(bootloader_file))
            should_enable = app_file_valid and bootloader_valid
        else:
            # When erase is disabled, bootloader is optional - just need app file
            should_enable = app_file_valid
        
        # Update button state
        if should_enable:
            self.program_button.config(state="normal")
            self.debug_log("Program button enabled")
        else:
            self.program_button.config(state="disabled")
            self.debug_log("Program button disabled")
            
            # Log why it's disabled for debugging
            if not app_file_valid:
                self.debug_log("  Reason: No valid application file selected")
            if erase_enabled and not bootloader_valid:
                self.debug_log("  Reason: Erase enabled but no valid bootloader file selected")
    
    def log(self, message, level="info"):
        """Add message to log window with color coding
        
        Args:
            message: Message to log
            level: Log level - "info", "success", "warning", "error"
        """
        # Add timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        # Insert with appropriate color tag
        start_pos = self.log_text.index(tk.END)
        self.log_text.insert(tk.END, formatted_message)
        
        if level != "info":
            # Apply color tag to the entire line
            line_start = f"{start_pos.split('.')[0]}.0"
            line_end = f"{int(start_pos.split('.')[0]) + 1}.0"
            self.log_text.tag_add(level, line_start, line_end)
        
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def log_success(self, message):
        """Log success message in green"""
        self.log(message, "success")
    
    def log_warning(self, message):
        """Log warning message in orange"""
        self.log(message, "warning")
    
    def log_error(self, message):
        """Log error message in red"""
        self.log(message, "error")
    
    def clear_log(self):
        """Clear the log window"""
        self.log_text.delete(1.0, tk.END)
    
    def run_commander_command(self, command):
        """Run a commander command and return output
        
        Args:
            command: List of command arguments to pass to subprocess
            
        Returns:
            tuple: (success: bool, stdout: str, stderr: str)
        """
        # Check if commander is available
        if not self.check_commander_available():
            return False, "", "Commander not available"
        
        # Replace 'commander' with actual path
        if command[0] == "commander":
            command[0] = self.commander_path
        
        self.debug_log(f"Command to execute: {command}")
        self.debug_log(f"Working directory: {os.getcwd()}")
        self.debug_log(f"Commander path: {self.commander_path}")
        
        try:
            self.debug_log(f"Running command: {' '.join(command)}")
            
            self.debug_log(f"Timeout set to: {self.COMMANDER_TIMEOUT} seconds")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.COMMANDER_TIMEOUT
            )
            
            self.debug_log(f"Command return code: {result.returncode}")
            self.debug_log(f"Command execution time: subprocess completed")
            
            # Log stdout
            if result.stdout:
                self.debug_log(result.stdout)
            else:
                self.debug_log("No stdout output")
            
            # Log stderr
            if result.stderr:
                self.debug_log(result.stderr)
            else:
                self.debug_log("No stderr output")
            
            success = result.returncode == 0
            self.debug_log(f"Command success: {success}")
            
            return success, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.log(f"ERROR: Command timed out after {self.COMMANDER_TIMEOUT} seconds")
            self.debug_log("Timeout exception caught")
            return False, "", "Timeout"
        except FileNotFoundError:
            self.log("ERROR: 'commander' not found. Please ensure Simplicity Commander is installed and in PATH")
            self.debug_log("FileNotFoundError exception caught")
            return False, "", "Commander not found"
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            self.debug_log(f"Unexpected exception: {type(e).__name__}: {str(e)}")
            return False, "", str(e)
    
    def verify_app_version(self, device_display, app_file=None):
        """Verify application version using commander readmem and util appinfo
        
        Args:
            device_display: The display device name selected by user
            app_file: The application filename to extract expected version from
            
        Returns:
            bool: True if verification succeeded, False otherwise
        """
        self.log("\n=== Verifying Application Version ===")
        
        # Get the actual device name for commander
        device = self.get_actual_device_name(device_display)
        self.log(f"Device: {device_display} ({device})")
        
        # Extract expected version from filename if provided
        expected_version = None
        expected_decimal = None
        if app_file:
            self.debug_log(f"Analyzing filename: {app_file}")
            expected_version, expected_decimal = self.extract_version_from_filename(app_file)
            if expected_version:
                self.debug_log(f"Expected version from filename: {expected_version} (decimal: {expected_decimal})")
            else:
                self.debug_log(f"Version extraction failed for filename: {app_file}")
        else:
            self.debug_log("No app file provided for version comparison")
        
        # Create temporary file for device dump
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.bin', delete=False) as tmp_file:
            dump_file = tmp_file.name
        
        self.debug_log(f"Created temporary dump file: {dump_file}")
        
        try:
            # Read device memory
            readmem_cmd = [
                "commander", "readmem",
                "--region", "@mainflash",
                "--outfile", dump_file,
                "--device", device
            ]
            
            self.debug_log("Starting device memory read operation")
            success, stdout, stderr = self.run_commander_command(readmem_cmd)
            
            if not success:
                self.log("ERROR: Failed to read device memory")
                self.debug_log(f"Memory read failed - stdout: {stdout}, stderr: {stderr}")
                return False
            
            self.debug_log("Device memory read completed successfully")
            
            # Get application info
            appinfo_cmd = ["commander", "util", "appinfo", dump_file]
            self.debug_log("Starting application info extraction")
            success, stdout, stderr = self.run_commander_command(appinfo_cmd)
            
            if success:
                self.debug_log(f"Application info extraction successful, processing {len(stdout.split())} lines of output")
                
                # Parse and highlight app version - only validate the FIRST app version found
                version_found = False
                version_matches = False
                first_version_processed = False
                device_versions = []  # Store all versions found on device
                
                for line_num, line in enumerate(stdout.split('\n'), 1):
                    if 'App version' in line:
                        self.debug_log(f"Found app version line {line_num}: {line.strip()}")
                        version_found = True
                        original_line, parsed_version, decimal_value = self.parse_app_version(line)
                        
                        self.log(f">>> {original_line.strip()} <<<")
                        
                        if parsed_version and decimal_value:
                            self.debug_log(f">>> Parsed Version: {parsed_version} (decimal: {decimal_value}) <<<")
                            self.debug_log(f"Version parsing successful: {parsed_version}, decimal: {decimal_value}")
                            device_versions.append((parsed_version, decimal_value))
                            
                            # Calculate alternative parse (int math) for comparison
                            int_version = None
                            if decimal_value >= 1000000:
                                int_major = decimal_value // 1000000
                                int_minor = (decimal_value % 1000000) // 1000
                                int_patch = decimal_value % 1000
                                int_version = f"{int_major}.{int_minor}.{int_patch}"
                                if int_version != parsed_version:
                                    self.debug_log(f">>> Alternative parse (int math): {int_version} <<<")
                                    self.debug_log(f"Alternative parsing: {int_version} vs byte parsing: {parsed_version}")
                            
                            # Only validate the FIRST app version against the filename
                            if not first_version_processed and expected_version and expected_decimal:
                                self.debug_log("Processing first app version for validation")
                                first_version_processed = True
                                version_match = False
                                match_reason = ""
                                comparison_version = None
                                
                                # Use int math version for comparison if available and different from byte parsing
                                if int_version and int_version != parsed_version:
                                    comparison_version = int_version
                                    match_type = "int math"
                                    self.debug_log(f"Using int math version for comparison: {int_version}")
                                else:
                                    comparison_version = parsed_version  
                                    match_type = "byte parsing"
                                    self.debug_log(f"Using byte parsing version for comparison: {parsed_version}")
                                
                                # Compare using string comparison
                                if comparison_version == expected_version:
                                    version_match = True
                                    match_reason = f"string match ({match_type})"
                                # Handle case where device has extra .0 (e.g., "10.20.30.0" vs "10.20.30")
                                elif comparison_version.endswith('.0') and comparison_version[:-2] == expected_version:
                                    version_match = True
                                    match_reason = f"string match (ignoring trailing .0, {match_type})"
                                # Handle case where expected has extra .0
                                elif expected_version.endswith('.0') and expected_version[:-2] == comparison_version:
                                    version_match = True
                                    match_reason = f"string match (ignoring expected trailing .0, {match_type})"
                                
                                self.debug_log(f"Version comparison: {comparison_version} vs {expected_version} = {version_match}")
                                
                                if version_match:
                                    self.log(f">>> ✓ VERSION MATCH: Device version {comparison_version} matches filename version {expected_version} <<<")
                                    self.debug_log(f"Version match confirmed: {comparison_version} == {expected_version} ({match_reason})")
                                    version_matches = True
                                    break
                                else:
                                    self.log(f">>> ✗ VERSION MISMATCH: Expected {expected_version} but device has {comparison_version} ({match_type}) <<<")
                            elif first_version_processed:
                                self.debug_log(f"Secondary app version found (not validated): {parsed_version}")
                                # Show alternative parsing for secondary versions but don't validate
                                if decimal_value >= 1000000:
                                    int_major = decimal_value // 1000000
                                    int_minor = (decimal_value % 1000000) // 1000
                                    int_patch = decimal_value % 1000
                                    int_version_secondary = f"{int_major}.{int_minor}.{int_patch}"
                                    if int_version_secondary != parsed_version:
                                        self.log(f">>> Alternative parse (int math): {int_version_secondary} <<<")
                                self.log(">>> (Secondary app version - not validated) <<<")
                        else:
                            self.log(">>> Could not parse version number <<<")
                            self.debug_log(f"Version parsing failed for line: {line.strip()}")
                            if not first_version_processed and expected_version:
                                first_version_processed = True
                                self.log(f">>> ✗ VERSION MISMATCH: Could not parse device version, expected {expected_version} <<<")
                
                self.debug_log(f"Version processing complete. Found {len(device_versions)} versions on device")
                
                # Summary of version verification (only for the first version)
                if version_found:
                    if expected_version:
                        if version_matches:
                            self.log(">>> ✓ VERSION VERIFICATION PASSED: Device version matches filename! <<<")
                            self.debug_log("Version verification PASSED")
                        else:
                            self.log(">>> ✗ VERSION VERIFICATION FAILED: Device version does not match filename! <<<")
                            self.debug_log("Version verification FAILED")
                            return False  # Return false on version mismatch
                    else:
                        self.log("Application version verified successfully!")
                        self.debug_log("Version verification completed (no filename comparison)")
                    return True
                else:
                    self.log("No application version found in output")
                    self.debug_log("No app version found in commander output")
                    return False
            else:
                self.log("ERROR: Failed to get application info")
                self.debug_log(f"Application info failed - stdout: {stdout}, stderr: {stderr}")
                return False
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(dump_file):
                    os.remove(dump_file)
                    self.debug_log(f"Temporary file removed: {dump_file}")
            except (OSError, PermissionError) as e:
                self.log(f"Warning: Could not remove temporary file {dump_file}: {e}")
                self.debug_log(f"Failed to remove temporary file: {e}")
    
    def parse_app_version(self, version_line):
        """Parse application version from hex to decimal and format as version string
        
        Args:
            version_line: String containing the app version line from commander output
            
        Returns:
            tuple: (original_line, parsed_version, decimal_value) or (original_line, None, None) if parsing fails
        """
        import re
        
        self.debug_log(f"Parsing version line: {version_line.strip()}")
        
        # Look for hex values in the line (e.g., 0x01010005, 0x1010005, etc.)
        hex_pattern = r'0x([0-9a-fA-F]+)'
        hex_matches = re.findall(hex_pattern, version_line)
        
        if not hex_matches:
            self.debug_log("No hex pattern (0x...) found, trying alternative pattern")
            # Try to find just hex digits after common prefixes
            hex_pattern = r'(?:version[:\s]+|v[:\s]*)?([0-9a-fA-F]{6,8})'
            hex_matches = re.findall(hex_pattern, version_line, re.IGNORECASE)
        
        if hex_matches:
            # Use the first hex value found
            hex_value = hex_matches[0]
            self.debug_log(f"Found hex value: {hex_value}")
            
            try:
                # Convert hex to decimal
                decimal_value = int(hex_value, 16)
                self.debug_log(f"Hex to decimal conversion: {hex_value} -> {decimal_value}")
                
                # Try to parse as byte-structured version first (e.g., 0x01010005 = v1.1.5)
                if len(hex_value) >= 6:  # At least 6 hex digits
                    # Pad to 8 digits if needed
                    padded_hex = hex_value.zfill(8)
                    self.debug_log(f"Padded hex: {padded_hex}")
                    
                    # Extract bytes: 0x01010005 -> 01, 01, 00, 05
                    byte3 = int(padded_hex[0:2], 16)  # Major version
                    byte2 = int(padded_hex[2:4], 16)  # Minor version  
                    byte1 = int(padded_hex[4:6], 16)  # Usually 0
                    byte0 = int(padded_hex[6:8], 16)  # Patch version
                    
                    self.debug_log(f"Byte extraction: {byte3}.{byte2}.{byte1}.{byte0}")
                    
                    # Format as version string
                    if byte1 == 0:  # Standard case: major.minor.patch
                        parsed_version = f"{byte3}.{byte2}.{byte0}"
                        self.debug_log(f"Standard 3-part version: {parsed_version}")
                    else:  # Include all components
                        parsed_version = f"{byte3}.{byte2}.{byte1}.{byte0}"
                        self.debug_log(f"4-part version: {parsed_version}")
                else:
                    self.debug_log("Hex value too short, using fallback decimal parsing")
                    # Fallback: Parse decimal as version (assuming format: major*1000000 + minor*1000 + patch)
                    if decimal_value >= 1000000:
                        major = decimal_value // 1000000
                        minor = (decimal_value % 1000000) // 1000
                        patch = decimal_value % 1000
                        parsed_version = f"{major}.{minor}.{patch}"
                        self.debug_log(f"Decimal math version: {parsed_version}")
                    else:
                        # Handle smaller values
                        if decimal_value >= 1000:
                            major = decimal_value // 1000
                            minor = decimal_value % 1000
                            parsed_version = f"{major}.{minor}"
                            self.debug_log(f"2-part version: {parsed_version}")
                        else:
                            parsed_version = str(decimal_value)
                            self.debug_log(f"Single number version: {parsed_version}")
                
                self.debug_log(f"Final parsed version: {parsed_version}, decimal: {decimal_value}")
                return version_line, parsed_version, decimal_value
            except ValueError as e:
                self.debug_log(f"ValueError during hex conversion: {e}")
        else:
            self.debug_log("No hex values found in version line")
        
        self.debug_log("Version parsing failed")
        return version_line, None, None
    
    def extract_version_from_filename(self, filename):
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
    
    def program_device_thread(self):
        """Thread function to program the device"""
        try:
            self.debug_log("Programming thread started")
            
            device_display = self.device_var.get()
            device = self.get_actual_device_name(device_display)
            app_file = self.app_file_var.get()
            bootloader_file = self.bootloader_file_var.get()
            erase_before_flash = self.erase_before_flash.get()
            
            self.debug_log(f"Programming parameters:")
            self.debug_log(f"  Device display: {device_display}")
            self.debug_log(f"  Device actual: {device}")
            self.debug_log(f"  App file: {app_file}")
            self.debug_log(f"  Bootloader file: {bootloader_file}")
            self.debug_log(f"  Erase before flash: {erase_before_flash}")
            
            # Validate inputs
            if not device_display:
                self.log("ERROR: Please select a device")
                self.debug_log("Validation failed: No device selected")
                return
            
            if not app_file:
                self.log("ERROR: Please select an application file")
                self.debug_log("Validation failed: No application file selected")
                return
            
            if not os.path.exists(app_file):
                self.log(f"ERROR: Application file not found: {app_file}")
                self.debug_log(f"Validation failed: Application file does not exist: {app_file}")
                return
            
            # Check if bootloader is required when erase is enabled
            if erase_before_flash and not bootloader_file:
                self.log("ERROR: Bootloader file is required when 'Erase Before Flash' is enabled")
                self.debug_log("Validation failed: Erase enabled but no bootloader file provided")
                return
            
            if bootloader_file and not os.path.exists(bootloader_file):
                self.log(f"ERROR: Bootloader file not found: {bootloader_file}")
                self.debug_log(f"Validation failed: Bootloader file does not exist: {bootloader_file}")
                return
            
            self.debug_log("Input validation passed")
            
            self.log("\n" + "="*60)
            self.log("Starting device programming...")
            self.log(f"Device: {device_display} ({device})")
            if erase_before_flash:
                self.log("Erase before flash: ENABLED")
            self.log("="*60)
            
            # Mass erase if requested
            if erase_before_flash:
                self.debug_log("Mass erase sequence initiated")
                self.log("\n=== Mass Erasing Device ===")
                erase_cmd = [
                    self.commander_path, "device", "masserase",
                    "--device", device
                ]
                
                self.debug_log(f"Mass erase command: {erase_cmd}")
                success, stdout, stderr = self.run_commander_command(erase_cmd)
                
                if not success:
                    self.log("ERROR: Failed to mass erase device")
                    self.log("Aborting programming sequence")
                    self.debug_log("Mass erase failed, aborting")
                    return
                
                self.log("Device mass erased successfully!")
                self.debug_log("Mass erase completed successfully")
            
            # Program bootloader if provided
            if bootloader_file:
                self.debug_log("Programming bootloader sequence initiated")
                self.log("\n=== Programming Bootloader ===")
                boot_cmd = [
                    self.commander_path, "flash",
                    bootloader_file,
                    "--device", device
                ]
                
                self.debug_log(f"Bootloader command: {boot_cmd}")
                success, stdout, stderr = self.run_commander_command(boot_cmd)
                
                if not success:
                    self.log("ERROR: Failed to program bootloader")
                    self.log("Aborting programming sequence")
                    self.debug_log("Bootloader programming failed, aborting")
                    return
                
                self.log("Bootloader programmed successfully!")
                self.debug_log("Bootloader programming completed successfully")
            else:
                self.debug_log("No bootloader file provided, skipping bootloader programming")
            
            # Program application
            self.debug_log("Programming application sequence initiated")
            self.log("\n=== Programming Application ===")
            app_cmd = [
                self.commander_path, "flash",
                app_file,
                "--device", device
            ]
            
            self.debug_log(f"Application command: {app_cmd}")
            success, stdout, stderr = self.run_commander_command(app_cmd)
            
            if not success:
                self.log("ERROR: Failed to program application")
                self.debug_log("Application programming failed")
                return
            
            self.log("Application programmed successfully!")
            self.debug_log("Application programming completed successfully")
            
            # Verify application version
            self.debug_log("Starting application version verification")
            self.verify_app_version(device_display, app_file)
            
            self.log("\n" + "="*60)
            self.log("Programming completed successfully!")
            self.log("="*60 + "\n")
            
        except Exception as e:
            self.log(f"ERROR: Unexpected error: {str(e)}")
            self.debug_log(f"Programming thread exception: {type(e).__name__}: {str(e)}")
            messagebox.showerror("Error", f"Programming failed: {str(e)}")
        finally:
            # Re-enable the program button
            self.program_button.config(state="normal")
            self.debug_log("Program button re-enabled")
    
    def program_device(self):
        """Start programming the device in a separate thread"""
        # Check if commander is available before starting
        if not self.check_commander_available():
            return
        
        # Disable the program button to prevent multiple clicks
        self.program_button.config(state="disabled")
        
        # Run programming in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.program_device_thread, daemon=True)
        thread.start()
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.current_theme = new_theme
        
        # Recreate the entire interface with new theme
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Reapply theme and recreate widgets
        self.style = ModernTheme.configure_modern_style(self.root, theme=new_theme)
        self.create_widgets()
        
        self.log_success(f"Theme changed to {new_theme} mode")
    
    def increase_font_size(self):
        """Increase application font size"""
        if self.current_font_size < 16:
            self.current_font_size += 1
            self.update_font_sizes()
            self.log_success(f"Font size increased to {self.current_font_size}")
    
    def decrease_font_size(self):
        """Decrease application font size"""
        if self.current_font_size > 8:
            self.current_font_size -= 1
            self.update_font_sizes()
            self.log_success(f"Font size decreased to {self.current_font_size}")
    
    def reset_font_size(self):
        """Reset font size to default"""
        self.current_font_size = 10
        self.update_font_sizes()
        self.log_success("Font size reset to default")
    
    def update_font_sizes(self):
        """Update all font sizes to current setting"""
        # Update various UI elements with new font size
        try:
            if hasattr(self, 'log_text'):
                self.log_text.configure(font=('Consolas', self.current_font_size - 1))
            if hasattr(self, 'device_combo'):
                self.device_combo.configure(font=('Segoe UI', self.current_font_size))
        except:
            pass
    
    def show_about(self):
        """Show application about dialog"""
        about_text = """Zigbee Device Programmer
        
A modern GUI application for programming Zigbee devices using Silicon Labs Simplicity Commander.

Features:
• Modern dark/light theme interface
• Device version verification
• Mass erase before programming
• JSON device mapping configuration
• Debug mode for detailed logging
• Commander status checking

Version: 2.0
Built with Python and tkinter"""
        
        messagebox.showinfo("About Zigbee Device Programmer", about_text)


def main():
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
