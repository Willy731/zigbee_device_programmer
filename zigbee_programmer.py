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

# Import our custom modules
from ui_theme import ModernTheme
from device_manager import DeviceMappingManager
from commander_manager import CommanderManager
from version_parser import VersionParser
from file_operations import FileOperationsManager

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
        
        # Debug mode for verbose logging (must be set before loading device mapping)
        self.debug_mode = False
        
        # Initialize manager instances
        self.device_manager = DeviceMappingManager(debug_callback=self.debug_log)
        self.commander_manager = CommanderManager(debug_callback=self.debug_log, status_callback=self.update_status)
        self.version_parser = VersionParser(debug_callback=self.debug_log)
        self.file_operations = FileOperationsManager(debug_callback=self.debug_log, version_parser=self.version_parser)
        
        # Initialize custom mapping path after device manager is created
        self.custom_mapping_path = None
        
        # Settings file for persistent configuration
        self.settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zigbee_programmer_settings.json")
        
        # Load device mapping from JSON using device manager
        self.device_manager.load_device_mapping()
        
        # Display names for the dropdown
        self.device_display_names = self.device_manager.get_device_display_names()
        
        # Find commander executable on startup using commander manager
        commander_paths = self.commander_manager.find_commander_paths()
        if commander_paths:
            self.commander_manager.set_commander_path(commander_paths[0])
        
        self.create_widgets()
        
    
    
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
        if not self.commander_manager.validate_commander_path():
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
        version_info = self.commander_manager.get_commander_version()
        if "Error" in version_info:
            error_msg = (
                f"Commander found but failed to execute.\n\n"
                f"Error: {version_info}\n\n"
                "Possible issues:\n"
                "1. Insufficient permissions - try running as administrator\n"
                "2. Missing dependencies\n"
                "3. Corrupted installation\n\n"
                "Please reinstall Simplicity Commander or contact support."
            )
            messagebox.showerror("Commander Execution Error", error_msg)
            self.log(f"ERROR: Commander execution failed: {version_info}")
            return False
        
        return True
    
    def get_theme_colors(self):
        """Get current theme colors"""
        if self.current_theme == "dark":
            return {
                'bg': ModernTheme.DARK_BG,
                'card_bg': ModernTheme.CARD_BG,
                'darker_bg': ModernTheme.DARKER_BG,
                'text_primary': ModernTheme.TEXT_PRIMARY,
                'text_secondary': ModernTheme.TEXT_SECONDARY,
                'border': ModernTheme.BORDER,
                'accent': ModernTheme.ACCENT,
                'success': ModernTheme.SUCCESS,
                'warning': ModernTheme.WARNING,
                'error': ModernTheme.ERROR
            }
        else:
            return {
                'bg': ModernTheme.LIGHT_BG,
                'card_bg': ModernTheme.LIGHT_CARD_BG,
                'darker_bg': ModernTheme.LIGHT_CARD_BG,
                'text_primary': ModernTheme.LIGHT_TEXT_PRIMARY,
                'text_secondary': ModernTheme.LIGHT_TEXT_SECONDARY,
                'border': ModernTheme.LIGHT_BORDER,
                'accent': ModernTheme.ACCENT,
                'success': ModernTheme.SUCCESS,
                'warning': ModernTheme.WARNING,
                'error': ModernTheme.ERROR
            }
        
    def create_widgets(self):
        # Get current theme colors
        colors = self.get_theme_colors()
        
        # Create modern menu bar
        self.create_menu()
        
        # Main container with modern styling
        main_container = tk.Frame(self.root, bg=colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header section (more compact)
        header_frame = tk.Frame(main_container, bg=colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = tk.Label(header_frame, 
                              text="Zigbee Device Programmer", 
                              font=('Segoe UI', 16, 'bold'),
                              fg=colors['text_primary'],
                              bg=colors['bg'])
        title_label.pack(side=tk.LEFT)
        
        # Main content area with cards
        content_frame = tk.Frame(main_container, bg=colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for configuration (scrollable, fixed width)
        left_panel_container = tk.Frame(content_frame, bg=colors['bg'], width=450)
        left_panel_container.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel_container.pack_propagate(False)
        
        # Create scrollable left panel
        self.create_scrollable_left_panel(left_panel_container, colors)
        
        # Right panel for log output (unchanged)
        right_panel = tk.Frame(content_frame, bg=colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Log Output Card
        self.create_log_output_card(right_panel)
        
        # Status bar at bottom
        self.create_modern_status_bar(main_container)
        
        # Initialize UI states after all widgets are created
        self.update_status()
        self.update_program_button_state()
    
    def create_scrollable_left_panel(self, parent, colors):
        """Create a scrollable left panel for configuration cards"""
        
        # Create canvas for scrollable content
        self.left_canvas = tk.Canvas(parent, 
                                    bg=colors['bg'],
                                    highlightthickness=0,
                                    bd=0,
                                    width=450)
        
        # Create vertical scrollbar for left panel
        left_scrollbar = tk.Scrollbar(parent, 
                                     orient=tk.VERTICAL, 
                                     command=self.left_canvas.yview,
                                     bg=colors['card_bg'],
                                     troughcolor=colors['darker_bg'],
                                     activebackground=colors['accent'])
        
        # Configure canvas scrolling
        self.left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        # Pack scrollbar and canvas
        left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create scrollable frame inside canvas
        self.left_scrollable_frame = tk.Frame(self.left_canvas, bg=colors['bg'])
        self.left_canvas_window = self.left_canvas.create_window((0, 0), 
                                                                window=self.left_scrollable_frame, 
                                                                anchor="nw")
        
        # Bind canvas configuration events
        self.left_scrollable_frame.bind("<Configure>", self.on_left_frame_configure)
        self.left_canvas.bind("<Configure>", self.on_left_canvas_configure)
        
        # Bind mouse wheel events for left panel scrolling
        self.bind_left_panel_mousewheel()
        
        # Create the configuration cards inside the scrollable frame
        self.create_device_config_card(self.left_scrollable_frame)
        self.create_file_selection_card(self.left_scrollable_frame)
        self.create_programming_options_card(self.left_scrollable_frame)
        self.create_action_buttons_card(self.left_scrollable_frame)
    
    def on_left_frame_configure(self, event):
        """Reset the scroll region for the left panel"""
        self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))
        
    def on_left_canvas_configure(self, event):
        """Configure the left panel canvas window size"""
        # Update the scrollable frame width to match canvas width
        canvas_width = event.width
        self.left_canvas.itemconfig(self.left_canvas_window, width=canvas_width)
    
    def bind_left_panel_mousewheel(self):
        """Bind mouse wheel events for left panel scrolling"""
        def on_left_mousewheel(event):
            # Only scroll if mouse is over the left canvas
            widget = event.widget
            # Check if the event is within the left canvas area
            if widget == self.left_canvas or self.is_widget_in_left_panel(widget):
                self.left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"  # Prevent event from propagating
            
        def is_descendant_of_left_canvas(widget):
            """Check if widget is a descendant of the left canvas"""
            while widget:
                if widget == self.left_canvas or widget == self.left_scrollable_frame:
                    return True
                widget = widget.master
            return False
        
        # Store the function as a method for later reference
        self.is_widget_in_left_panel = is_descendant_of_left_canvas
        
        # Bind mouse wheel events to left canvas and its children
        self.left_canvas.bind("<MouseWheel>", on_left_mousewheel)
        
        # For Linux (button 4 and 5)
        self.left_canvas.bind("<Button-4>", lambda e: self.left_canvas.yview_scroll(-1, "units"))
        self.left_canvas.bind("<Button-5>", lambda e: self.left_canvas.yview_scroll(1, "units"))
    
    def create_card_frame(self, parent, title, expand_vertical=False):
        """Create a modern card-style frame with title
        
        Args:
            parent: Parent widget
            title: Card title
            expand_vertical: If True, card will expand vertically to fill available space
        """
        # Get current theme colors
        colors = self.get_theme_colors()
        bg_color = colors['bg']
        card_bg = colors['card_bg']
        text_color = colors['text_primary']
        border_color = colors['border']
        
        # Card container (with optional vertical expansion)
        if expand_vertical:
            card_container = tk.Frame(parent, bg=bg_color)
            card_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        else:
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
        
        # Card content (with optional vertical expansion)
        if expand_vertical:
            content_frame = tk.Frame(card_container, bg=card_bg, bd=1, relief='solid')
            content_frame.pack(fill=tk.BOTH, expand=True)
        else:
            content_frame = tk.Frame(card_container, bg=card_bg, bd=1, relief='solid')
            content_frame.pack(fill=tk.X)
        content_frame.configure(highlightbackground=border_color, highlightcolor=border_color)
        
        return content_frame
    
    def create_device_config_card(self, parent):
        """Create device configuration card"""
        colors = self.get_theme_colors()
        card_content = self.create_card_frame(parent, "Device Configuration")
        
        # Device selection with modern styling (reduced padding)
        device_frame = tk.Frame(card_content, bg=colors['card_bg'])
        device_frame.pack(fill=tk.X, padx=15, pady=12)
        
        device_label = tk.Label(device_frame,
                               text="Target Device",
                               font=('Segoe UI', 9, 'bold'),
                               fg=colors['text_primary'],
                               bg=colors['card_bg'])
        device_label.pack(anchor=tk.W, pady=(0, 4))
        
        self.device_combo = ttk.Combobox(device_frame, 
                                        textvariable=self.device_var,
                                        values=self.device_display_names, 
                                        state="readonly",
                                        style="LightDevice.TCombobox",
                                        font=('Segoe UI', 10))
        self.device_combo.pack(fill=tk.X)
        if self.device_display_names:
            self.device_combo.current(0)
    
    def create_file_selection_card(self, parent):
        """Create file selection card"""
        colors = self.get_theme_colors()
        card_content = self.create_card_frame(parent, "File Selection")
        
        # Application file selection (reduced padding)
        app_frame = tk.Frame(card_content, bg=colors['card_bg'])
        app_frame.pack(fill=tk.X, padx=15, pady=(12, 8))
        
        app_label = tk.Label(app_frame,
                            text="Application File",
                            font=('Segoe UI', 9, 'bold'),
                            fg=colors['text_primary'],
                            bg=colors['card_bg'])
        app_label.pack(anchor=tk.W, pady=(0, 4))
        
        app_input_frame = tk.Frame(app_frame, bg=colors['card_bg'])
        app_input_frame.pack(fill=tk.X)
        
        self.app_entry = tk.Entry(app_input_frame,
                                 textvariable=self.app_file_var,
                                 font=('Segoe UI', 10),
                                 bg=colors['card_bg'],
                                 fg=colors['text_primary'],
                                 insertbackground=colors['text_primary'],
                                 bd=1,
                                 relief='solid',
                                 highlightthickness=1,
                                 highlightcolor=colors['accent'],
                                 highlightbackground=colors['border'])
        self.app_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        app_browse_btn = ttk.Button(app_input_frame,
                                   text="Browse",
                                   command=self.browse_app_file,
                                   style="Modern.TButton")
        app_browse_btn.pack(side=tk.RIGHT)
        
        # Bootloader file selection (reduced padding)
        boot_frame = tk.Frame(card_content, bg=colors['card_bg'])
        boot_frame.pack(fill=tk.X, padx=15, pady=(8, 12))
        
        boot_label_frame = tk.Frame(boot_frame, bg=colors['card_bg'])
        boot_label_frame.pack(fill=tk.X, pady=(0, 4))
        
        boot_label = tk.Label(boot_label_frame,
                             text="Bootloader File",
                             font=('Segoe UI', 9, 'bold'),
                             fg=colors['text_primary'],
                             bg=colors['card_bg'])
        boot_label.pack(side=tk.LEFT)
        
        self.bootloader_optional_label = tk.Label(boot_label_frame,
                                                  text="(Optional)",
                                                  font=('Segoe UI', 8, 'italic'),
                                                  fg=colors['text_secondary'],
                                                  bg=colors['card_bg'])
        self.bootloader_optional_label.pack(side=tk.LEFT, padx=(5, 0))
        
        boot_input_frame = tk.Frame(boot_frame, bg=colors['card_bg'])
        boot_input_frame.pack(fill=tk.X)
        
        self.boot_entry = tk.Entry(boot_input_frame,
                                  textvariable=self.bootloader_file_var,
                                  font=('Segoe UI', 10),
                                  bg=colors['card_bg'],
                                  fg=colors['text_primary'],
                                  insertbackground=colors['text_primary'],
                                  bd=1,
                                  relief='solid',
                                  highlightthickness=1,
                                  highlightcolor=colors['accent'],
                                  highlightbackground=colors['border'])
        self.boot_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        boot_browse_btn = ttk.Button(boot_input_frame,
                                    text="Browse",
                                    command=self.browse_bootloader_file,
                                    style="Modern.TButton")
        boot_browse_btn.pack(side=tk.RIGHT)
    
    def create_programming_options_card(self, parent):
        """Create programming options card"""
        colors = self.get_theme_colors()
        card_content = self.create_card_frame(parent, "Programming Options")
        
        options_frame = tk.Frame(card_content, bg=colors['card_bg'])
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
                             fg=colors['text_secondary'],
                             bg=colors['card_bg'])
        erase_info.pack(anchor=tk.W, pady=(3, 0))
    
    def create_action_buttons_card(self, parent):
        """Create action buttons card"""
        colors = self.get_theme_colors()
        card_content = self.create_card_frame(parent, "Actions")
        
        button_frame = tk.Frame(card_content, bg=colors['card_bg'])
        button_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # Primary program button
        self.program_button = ttk.Button(button_frame,
                                        text="Program Device",
                                        command=self.program_device,
                                        style="Primary.TButton")
        self.program_button.pack(fill=tk.X, pady=(0, 8))
        
        # Secondary action buttons
        secondary_frame = tk.Frame(button_frame, bg=colors['card_bg'])
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
        colors = self.get_theme_colors()
        card_content = self.create_card_frame(parent, "Log Output", expand_vertical=True)
        
        log_frame = tk.Frame(card_content, bg=colors['card_bg'])
        log_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        # Create custom styled text widget
        self.log_text = tk.Text(log_frame,
                               wrap=tk.WORD,
                               font=('Consolas', 9),
                               bg=colors['darker_bg'],
                               fg=colors['text_primary'],
                               insertbackground=colors['text_primary'],
                               selectbackground=colors['accent'],
                               selectforeground=colors['text_primary'],
                               bd=1,
                               relief='solid',
                               highlightthickness=0)
        
        # Create custom scrollbar
        scrollbar = tk.Scrollbar(log_frame,
                                bg=colors['card_bg'],
                                troughcolor=colors['darker_bg'],
                                activebackground=colors['accent'],
                                highlightthickness=0)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # Configure text tags for colored output
        self.log_text.tag_configure("success", foreground=colors['success'])
        self.log_text.tag_configure("warning", foreground=colors['warning'])
        self.log_text.tag_configure("error", foreground=colors['error'])
        self.log_text.tag_configure("info", foreground=colors['accent'])
    
    def create_modern_status_bar(self, parent):
        """Create modern status bar"""
        colors = self.get_theme_colors()
        status_frame = tk.Frame(parent, bg=colors['darker_bg'], height=25)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(status_frame,
                                    textvariable=self.status_var,
                                    font=('Segoe UI', 8),
                                    fg=colors['text_secondary'],
                                    bg=colors['darker_bg'],
                                    anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=12, pady=4)
        
    def create_menu(self):
        """Create the application menu with modern styling"""
        colors = self.get_theme_colors()
        menubar = tk.Menu(self.root,
                         bg=colors['card_bg'],
                         fg=colors['text_primary'],
                         activebackground=colors['accent'],
                         activeforeground=colors['text_primary'],
                         borderwidth=0)
        self.root.config(menu=menubar)
        
        # View menu for theme options
        view_menu = tk.Menu(menubar, tearoff=0,
                           bg=colors['card_bg'],
                           fg=colors['text_primary'],
                           activebackground=colors['accent'],
                           activeforeground=colors['text_primary'],
                           borderwidth=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark/Light Theme", command=self.toggle_theme)
        view_menu.add_separator()
        view_menu.add_command(label="Increase Font Size", command=self.increase_font_size)
        view_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size)
        view_menu.add_command(label="Reset Font Size", command=self.reset_font_size)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0,
                            bg=colors['card_bg'],
                            fg=colors['text_primary'],
                            activebackground=colors['accent'],
                            activeforeground=colors['text_primary'],
                            borderwidth=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Check Commander Status", command=self.check_commander_status)
        tools_menu.add_command(label="Set Commander Path...", command=self.set_commander_path)
        tools_menu.add_command(label="Test Device Connection", command=self.test_device_connection)
        tools_menu.add_separator()
        tools_menu.add_command(label="Select Device Mapping File...", command=self.select_device_mapping_wrapper)
        tools_menu.add_separator()
        tools_menu.add_command(label="Toggle Debug Mode", command=self.toggle_debug_mode)
        tools_menu.add_separator()
        tools_menu.add_command(label="Refresh Commander", command=self.refresh_commander)
        if platform.system() == "Windows":
            tools_menu.add_separator()
            tools_menu.add_command(label="Restart as Administrator", command=self.restart_as_admin)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0,
                           bg=colors['card_bg'],
                           fg=colors['text_primary'],
                           activebackground=colors['accent'],
                           activeforeground=colors['text_primary'],
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
            self.commander_manager.set_commander_path(filename)
            self.log(f"Commander path set to: {filename}")
            self.update_status()
            messagebox.showinfo("Success", f"Commander path updated to:\n{filename}")
    
    def refresh_commander(self):
        """Re-search for commander"""
        self.log("\n=== Searching for Simplicity Commander ===")
        commander_paths = self.commander_manager.find_commander_paths()
        if commander_paths:
            self.commander_manager.set_commander_path(commander_paths[0])
            self.log(f"Commander found at: {commander_paths[0]}")
            messagebox.showinfo("Success", f"Commander found at:\n{commander_paths[0]}")
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
        
        device = self.device_manager.get_actual_device_name(device_display)
        
        self.log("\n=== Testing Device Connection ===")
        self.log(f"Testing connection to device: {device_display} ({device})")
        
        # Test with device list command
        list_cmd = ["commander", "adapter", "list"]
        success, stdout, stderr = self.run_commander_command(list_cmd)
        
        if success:
            self.log("Device adapters found:")
            if "J-Link" in stdout or "adapter" in stdout.lower():
                self.log("✓ J-Link adapter detected")
                
                # Test device-specific connection
                probe_cmd = ["commander", "adapter", "probe", "--device", device]
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
        if self.commander_manager.validate_commander_path():
            commander_path = self.commander_manager.commander_path
            self.log(f"Commander found at: {commander_path}")
            
            # Test commander by getting version
            version_info = self.commander_manager.get_commander_version()
            if "Error" not in version_info:
                self.log("Commander is working correctly!")
                self.log(f"Version info: {version_info}")
            else:
                self.log("Commander found but may not be working correctly")
                self.log(f"Error: {version_info}")
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
        # Check if status_var exists (status bar has been created)
        if not hasattr(self, 'status_var'):
            return
            
        status_parts = []
        
        if self.commander_manager.validate_commander_path():
            status_parts.append("Commander available")
        else:
            status_parts.append("Commander NOT FOUND")
        
        # Add device mapping info  
        mapping_info = self.device_manager.get_mapping_info()
        status_parts.append(mapping_info)
        
        if platform.system() == "Windows":
            if self.is_admin():
                status_parts.append("Running as Administrator")
            else:
                status_parts.append("Running as User")
        
        if self.debug_mode:
            status_parts.append("DEBUG MODE")
        
        self.status_var.set(" | ".join(status_parts))
        
    def browse_app_file(self):
        success, selected_path, message = self.file_operations.browse_application_file(self.app_file_var)
        if success:
            self.log(f"Selected application file: {selected_path}")
            self.debug_log(f"Application file selected - path: {selected_path}")
        else:
            if message and message != "File selection cancelled":
                self.debug_log(f"Application file selection error: {message}")
            else:
                self.debug_log("Application file selection cancelled by user")
        
        # Update program button state
        self.update_program_button_state()
    
    def browse_bootloader_file(self):
        success, selected_path, message = self.file_operations.browse_bootloader_file(self.bootloader_file_var)
        if success:
            self.log(f"Selected bootloader file: {selected_path}")
            self.debug_log(f"Bootloader file selected - path: {selected_path}")
        else:
            if message and message != "File selection cancelled":
                self.debug_log(f"Bootloader file selection error: {message}")
            else:
                self.debug_log("Bootloader file selection cancelled by user")
        
        # Update program button state
        self.update_program_button_state()
    
    def select_device_mapping_wrapper(self):
        """Wrapper method for device mapping file selection"""
        success, message = self.device_manager.select_device_mapping_file(
            lambda: filedialog.askopenfilename(
                title="Select Device Mapping JSON File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
        )
        if success:
            # Update the UI with new device list
            self.device_display_names = self.device_manager.get_device_display_names()
            self.refresh_device_dropdown()
            self.log(message)
        elif message:
            self.debug_log(message)
    
    def on_erase_checkbox_changed(self):
        """Handle the erase before flash checkbox state change"""
        colors = self.get_theme_colors()
        if self.erase_before_flash.get():
            # When erase is checked, bootloader becomes mandatory
            self.bootloader_optional_label.config(text="(Required for Erase)", fg=colors['error'])
            self.debug_log("Erase before flash enabled - bootloader is now required")
        else:
            # When erase is unchecked, bootloader is optional again
            self.bootloader_optional_label.config(text="(Optional)", fg=colors['text_secondary'])
            self.debug_log("Erase before flash disabled - bootloader is now optional")
        
        # Update program button state
        self.update_program_button_state()
    
    def update_program_button_state(self):
        """Enable/disable the Program Device button based on current selections"""
        # Check if program_button exists (button has been created)
        if not hasattr(self, 'program_button'):
            return
            
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
        
        # Replace 'commander' with actual path from manager
        commander_path = self.commander_manager.commander_path
        if command[0] == "commander":
            command[0] = commander_path
        
        self.debug_log(f"Command to execute: {command}")
        self.debug_log(f"Working directory: {os.getcwd()}")
        self.debug_log(f"Commander path: {commander_path}")
        
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
    
    def program_device_thread(self):
        """Thread function to program the device"""
        try:
            self.debug_log("Programming thread started")
            
            device_display = self.device_var.get()
            device = self.device_manager.get_actual_device_name(device_display)
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
            
            tempString = ""
            if erase_before_flash:
                tempString = "Erase before flash: ENABLED\n"

            self.log("\n" + "="*60 + "\nStarting device programming..." + f"Device: {device_display} ({device})\n {tempString}" + "="*60)
            # Mass erase if requested
            if erase_before_flash:
                self.debug_log("Mass erase sequence initiated")
                self.log("\n=== Mass Erasing Device ===")
                erase_cmd = [
                    "commander", "device", "masserase",
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
                    "commander", "flash",
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
                "commander", "flash",
                app_file,
                "--device", device
            ]
            
            self.debug_log(f"Application command: {app_cmd}")
            success, stdout, stderr = self.run_commander_command(app_cmd)
            
            if not success:
                self.log("ERROR: Failed to program application")
                return
            
            self.log("Application programmed successfully!")
            
            # Verify application version using file operations manager
            self.debug_log("Starting application version verification")
            verification_result = self.file_operations.verify_application_version(
                device_display, app_file, self.device_manager
            )
            if verification_result['compatible']:
                self.log("\n" + "="*60 + f"\n  Version verification: {verification_result['message']}; Expected: {verification_result['version_info']['version']}\n"+"="*60 + "\n")
            else:
                self.log(f"Version verification warning: {verification_result['message']}; Expected: {verification_result['version_info']['version']}")
            for warning in verification_result.get('warnings', []):
                self.log(f"WARNING: {warning}")
            
            self.log("\n" + "="*60 + "\n   Programming completed successfully!\n"+"="*60 + "\n")
            
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

    # Backward compatibility methods for tests
    def extract_version_from_filename(self, filename):
        """Proxy to version_parser for backward compatibility"""
        return self.version_parser.extract_version_from_filename(filename)
    
    def verify_app_version(self, device_display, app_file_path):
        """Proxy to file_operations for backward compatibility"""
        return self.file_operations.verify_application_version(device_display, app_file_path, self.device_manager)
    
    def get_actual_device_name(self, display_name):
        """Proxy to device_manager for backward compatibility"""
        return self.device_manager.get_actual_device_name(display_name)
    
    def load_device_mapping(self):
        """Proxy to device_manager for backward compatibility"""
        return self.device_manager.load_device_mapping()
    
    def save_settings(self):
        """Proxy to device_manager for backward compatibility"""
        return self.device_manager.save_settings()
    
    def load_settings(self):
        """Proxy to device_manager for backward compatibility"""
        return self.device_manager.load_settings()
    
    def refresh_device_dropdown(self):
        """Refresh the device dropdown with current mapping"""
        device_names = self.device_manager.get_device_display_names()
        self.device_combo['values'] = device_names
        if device_names and not self.device_var.get():
            self.device_var.set(device_names[0])
    
    @property
    def device_display_names(self):
        """Proxy to device_manager for backward compatibility"""
        return self.device_manager.get_device_display_names()
    
    @device_display_names.setter
    def device_display_names(self, value):
        """Setter for device_display_names (no-op for backward compatibility)"""
        # This is just for compatibility - the actual names come from device_mapping
        pass
    
    @property
    def device_mapping(self):
        """Proxy to device_manager.device_mapping for backward compatibility"""
        return self.device_manager.get_device_mapping()
    
    @device_mapping.setter
    def device_mapping(self, value):
        """Setter for device_mapping to update the manager's mapping"""
        self.device_manager.device_mapping = value
    
    @property 
    def custom_mapping_path(self):
        """Proxy to device_manager.custom_mapping_path for backward compatibility"""
        return self.device_manager.custom_mapping_path
    
    @custom_mapping_path.setter
    def custom_mapping_path(self, value):
        """Setter for custom_mapping_path to update the manager's path"""
        self.device_manager.custom_mapping_path = value


def main():
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
