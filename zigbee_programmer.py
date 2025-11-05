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


class ZigbeeProgrammerGUI:
    # Constants
    COMMANDER_TIMEOUT = 120  # Timeout for commander commands in seconds
    
    def __init__(self, root):
        self.root = root
        self.root.title("Zigbee Device Programmer")
        self.root.geometry("800x600")
        
        # Variables
        self.device_var = tk.StringVar()
        self.app_file_var = tk.StringVar()
        self.bootloader_file_var = tk.StringVar()
        
        # Common Zigbee device types
        self.devices = [
            "EFR32MG12P432F1024GL125",
            "EFR32MG13P632F512GM48",
            "EFR32MG21A020F1024IM32",
            "EFR32MG24B210F1536IM48",
            "EFR32MG24B220F1536IM48",
            "EFR32MG24B310F1536IM48",
            "EFR32FG14P233F256GM48",
            "EFR32FG23A010F512GM48",
            "EFR32FG25B220F1920IM56",
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Device selection
        row = 0
        ttk.Label(main_frame, text="Device:").grid(row=row, column=0, sticky=tk.W, pady=5)
        device_combo = ttk.Combobox(main_frame, textvariable=self.device_var, 
                                     values=self.devices, state="readonly", width=40)
        device_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        if self.devices:
            device_combo.current(0)
        
        # Application file selection
        row += 1
        ttk.Label(main_frame, text="Application File:").grid(row=row, column=0, sticky=tk.W, pady=5)
        app_frame = ttk.Frame(main_frame)
        app_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        app_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(app_frame, textvariable=self.app_file_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(app_frame, text="Browse...", command=self.browse_app_file).grid(row=0, column=1, padx=(5, 0))
        
        # Bootloader file selection (optional)
        row += 1
        ttk.Label(main_frame, text="Bootloader File:").grid(row=row, column=0, sticky=tk.W, pady=5)
        boot_frame = ttk.Frame(main_frame)
        boot_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        boot_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(boot_frame, textvariable=self.bootloader_file_var).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(boot_frame, text="Browse...", command=self.browse_bootloader_file).grid(row=0, column=1, padx=(5, 0))
        ttk.Label(main_frame, text="(Optional)", font=("", 8, "italic")).grid(row=row, column=2, sticky=tk.W, padx=(5, 0))
        
        # Program button
        row += 1
        self.program_button = ttk.Button(main_frame, text="Program Device", command=self.program_device)
        self.program_button.grid(row=row, column=0, columnspan=3, pady=20)
        
        # Log window
        row += 1
        ttk.Label(main_frame, text="Log Output:").grid(row=row, column=0, sticky=tk.W, pady=(10, 5))
        
        row += 1
        log_frame = ttk.Frame(main_frame)
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        row += 1
        ttk.Button(main_frame, text="Clear Log", command=self.clear_log).grid(row=row, column=0, columnspan=3, pady=5)
        
    def browse_app_file(self):
        filename = filedialog.askopenfilename(
            title="Select Application File",
            filetypes=[
                ("Binary Files", "*.bin *.hex *.s37"),
                ("All Files", "*.*")
            ]
        )
        if filename:
            self.app_file_var.set(filename)
            self.log(f"Selected application file: {filename}")
    
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
    
    def log(self, message):
        """Add message to log window"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
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
        try:
            self.log(f"Running command: {' '.join(command)}")
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.COMMANDER_TIMEOUT
            )
            
            # Log stdout
            if result.stdout:
                self.log(result.stdout)
            
            # Log stderr
            if result.stderr:
                self.log(result.stderr)
            
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.log(f"ERROR: Command timed out after {self.COMMANDER_TIMEOUT} seconds")
            return False, "", "Timeout"
        except FileNotFoundError:
            self.log("ERROR: 'commander' not found. Please ensure Simplicity Commander is installed and in PATH")
            return False, "", "Commander not found"
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            return False, "", str(e)
    
    def verify_app_version(self, device):
        """Verify application version using commander readmem and util appinfo
        
        Args:
            device: The device name/model to read from
            
        Returns:
            bool: True if verification succeeded, False otherwise
        """
        self.log("\n=== Verifying Application Version ===")
        
        # Create temporary file for device dump
        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.bin', delete=False) as tmp_file:
            dump_file = tmp_file.name
        
        try:
            # Read device memory
            readmem_cmd = [
                "commander", "readmem",
                "--region", "@mainflash",
                "--outfile", dump_file,
                "--device", device
            ]
            
            success, stdout, stderr = self.run_commander_command(readmem_cmd)
            
            if not success:
                self.log("ERROR: Failed to read device memory")
                return False
            
            # Get application info
            appinfo_cmd = ["commander", "util", "appinfo", dump_file]
            success, stdout, stderr = self.run_commander_command(appinfo_cmd)
            
            if success:
                # Parse and highlight app version
                for line in stdout.split('\n'):
                    if 'App version' in line:
                        self.log(f">>> {line.strip()} <<<")
                self.log("Application version verified successfully!")
                return True
            else:
                self.log("ERROR: Failed to get application info")
                return False
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(dump_file):
                    os.remove(dump_file)
            except (OSError, PermissionError) as e:
                self.log(f"Warning: Could not remove temporary file {dump_file}: {e}")
    
    def program_device_thread(self):
        """Thread function to program the device"""
        try:
            device = self.device_var.get()
            app_file = self.app_file_var.get()
            bootloader_file = self.bootloader_file_var.get()
            
            # Validate inputs
            if not device:
                self.log("ERROR: Please select a device")
                return
            
            if not app_file:
                self.log("ERROR: Please select an application file")
                return
            
            if not os.path.exists(app_file):
                self.log(f"ERROR: Application file not found: {app_file}")
                return
            
            if bootloader_file and not os.path.exists(bootloader_file):
                self.log(f"ERROR: Bootloader file not found: {bootloader_file}")
                return
            
            self.log("\n" + "="*60)
            self.log("Starting device programming...")
            self.log("="*60)
            
            # Program bootloader if provided
            if bootloader_file:
                self.log("\n=== Programming Bootloader ===")
                boot_cmd = [
                    "commander", "flash",
                    bootloader_file,
                    "--device", device
                ]
                success, stdout, stderr = self.run_commander_command(boot_cmd)
                
                if not success:
                    self.log("ERROR: Failed to program bootloader")
                    self.log("Aborting programming sequence")
                    return
                
                self.log("Bootloader programmed successfully!")
            
            # Program application
            self.log("\n=== Programming Application ===")
            app_cmd = [
                "commander", "flash",
                app_file,
                "--device", device
            ]
            success, stdout, stderr = self.run_commander_command(app_cmd)
            
            if not success:
                self.log("ERROR: Failed to program application")
                return
            
            self.log("Application programmed successfully!")
            
            # Verify application version
            self.verify_app_version(device)
            
            self.log("\n" + "="*60)
            self.log("Programming completed successfully!")
            self.log("="*60 + "\n")
            
            messagebox.showinfo("Success", "Device programmed successfully!")
            
        except Exception as e:
            self.log(f"ERROR: Unexpected error: {str(e)}")
            messagebox.showerror("Error", f"Programming failed: {str(e)}")
        finally:
            # Re-enable the program button
            self.program_button.config(state="normal")
    
    def program_device(self):
        """Start programming the device in a separate thread"""
        # Disable the program button to prevent multiple clicks
        self.program_button.config(state="disabled")
        
        # Run programming in a separate thread to keep UI responsive
        thread = threading.Thread(target=self.program_device_thread, daemon=True)
        thread.start()


def main():
    root = tk.Tk()
    app = ZigbeeProgrammerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
