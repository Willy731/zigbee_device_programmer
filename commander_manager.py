#!/usr/bin/env python3
"""
Commander Operations Manager
Handles all Silicon Labs Commander interactions for Zigbee device programming
"""

import subprocess
import threading
import re
import os
import tempfile
from tkinter import messagebox


class CommanderManager:
    """Manages Silicon Labs Commander operations"""
    
    def __init__(self, debug_callback=None, status_callback=None):
        self.debug_log = debug_callback or (lambda msg: None)
        self.update_status = status_callback or (lambda msg: None)
        self.commander_path = None
        self.current_device = None
        self.current_process = None
        self.should_stop = False
        
    def find_commander_paths(self):
        """Find all available Commander executable paths"""
        search_paths = [
            "C:\\SiliconLabs\\SimplicityStudio\\v5\\developer\\adapter_packs\\commander\\",
            "C:\\Program Files\\SiliconLabs\\SimplicityStudio\\v5\\developer\\adapter_packs\\commander\\",
            "C:\\Program Files (x86)\\SiliconLabs\\SimplicityStudio\\v5\\developer\\adapter_packs\\commander\\",
            "C:\\SiliconLabs\\SimplicityStudio\\v4\\developer\\adapter_packs\\commander\\",
            "C:\\Program Files\\SiliconLabs\\SimplicityStudio\\v4\\developer\\adapter_packs\\commander\\",
            "C:\\Program Files (x86)\\SiliconLabs\\SimplicityStudio\\v4\\developer\\adapter_packs\\commander\\",
            "C:\\SiliconLabs\\SimplicityStudio\\developer\\adapter_packs\\commander\\",
            "C:\\Program Files\\SiliconLabs\\SimplicityStudio\\developer\\adapter_packs\\commander\\",
            "C:\\Program Files (x86)\\SiliconLabs\\SimplicityStudio\\developer\\adapter_packs\\commander\\",
        ]
        
        found_paths = []
        for base_path in search_paths:
            if os.path.exists(base_path):
                commander_exe = os.path.join(base_path, "commander.exe")
                if os.path.exists(commander_exe):
                    found_paths.append(commander_exe)
        
        # Also check if commander is in PATH
        try:
            result = subprocess.run(["where", "commander"], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                paths_in_env = result.stdout.strip().split('\n')
                found_paths.extend([p.strip() for p in paths_in_env if p.strip()])
        except Exception:
            pass
        
        # Remove duplicates while preserving order
        unique_paths = []
        for path in found_paths:
            normalized_path = os.path.normpath(path)
            if normalized_path not in unique_paths:
                unique_paths.append(normalized_path)
        
        return unique_paths
    
    def set_commander_path(self, path):
        """Set the path to commander executable"""
        self.commander_path = path
        self.debug_log(f"Commander path set to: {path}")
    
    def validate_commander_path(self):
        """Validate that commander path is set and executable exists"""
        if not self.commander_path:
            self.debug_log("No commander path selected")
            return False
        
        if not os.path.exists(self.commander_path):
            self.debug_log(f"Commander not found at: {self.commander_path}")
            return False
        
        return True
    
    def get_commander_version(self):
        """Get commander version information"""
        if not self.validate_commander_path():
            return "Commander not available"
        
        try:
            cmd = [self.commander_path, "--version"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Parse version from output
                version_line = result.stdout.strip().split('\n')[0]
                return version_line
            else:
                return f"Error getting version: {result.stderr}"
        except Exception as e:
            return f"Error: {e}"
    
    def parse_j_link_info(self, output):
        """Parse J-Link probe information from commander output"""
        j_link_pattern = r"J-Link\[(\d+)\]: (\d+) \((\w+)\)"
        j_links = re.findall(j_link_pattern, output)
        
        parsed_j_links = []
        for match in j_links:
            index, serial, product = match
            parsed_j_links.append({
                'index': int(index),
                'serial': serial,
                'product': product,
                'display': f"[{index}] {serial} ({product})"
            })
        
        return parsed_j_links
    
    def get_j_link_probes(self):
        """Get list of available J-Link probes"""
        if not self.validate_commander_path():
            return []
        
        try:
            cmd = [self.commander_path, "adapter", "probe"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return self.parse_j_link_info(result.stdout)
            else:
                self.debug_log(f"Error getting J-Link probes: {result.stderr}")
                return []
        except Exception as e:
            self.debug_log(f"Error running commander: {e}")
            return []
    
    def flash_firmware(self, gbl_file, device_name, j_link_serial=None, progress_callback=None):
        """Flash firmware to device"""
        if not self.validate_commander_path():
            return False, "Commander not available"
        
        if not gbl_file or not os.path.exists(gbl_file):
            return False, "GBL file not found"
        
        self.current_device = device_name
        self.should_stop = False
        
        # Build command
        cmd = [self.commander_path, "flash", gbl_file, "--device", device_name]
        
        if j_link_serial:
            cmd.extend(["--serialno", j_link_serial])
        
        self.debug_log(f"Starting flash command: {' '.join(cmd)}")
        
        try:
            # Start process in a separate thread to allow for cancellation
            result_container = {'success': False, 'error': None}
            
            def flash_thread():
                try:
                    self.current_process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        universal_newlines=True
                    )
                    
                    output_lines = []
                    while True:
                        if self.should_stop:
                            self.current_process.terminate()
                            result_container['error'] = "Operation cancelled by user"
                            break
                        
                        output = self.current_process.stdout.readline()
                        if output == '' and self.current_process.poll() is not None:
                            break
                        
                        if output:
                            output_lines.append(output.strip())
                            self.debug_log(f"Commander: {output.strip()}")
                            
                            # Update progress if callback provided
                            if progress_callback:
                                progress_callback(output.strip())
                    
                    # Wait for process to complete
                    self.current_process.wait()
                    
                    if not self.should_stop:
                        if self.current_process.returncode == 0:
                            result_container['success'] = True
                        else:
                            result_container['error'] = '\n'.join(output_lines[-10:])  # Last 10 lines
                    
                except Exception as e:
                    result_container['error'] = str(e)
                finally:
                    self.current_process = None
            
            # Start flash thread
            thread = threading.Thread(target=flash_thread)
            thread.daemon = True
            thread.start()
            
            # Wait for completion (with timeout)
            thread.join(timeout=300)  # 5 minute timeout
            
            if thread.is_alive():
                self.should_stop = True
                thread.join(timeout=5)
                return False, "Operation timed out"
            
            if result_container['success']:
                return True, "Flash completed successfully"
            else:
                error_msg = result_container['error'] or "Unknown error occurred"
                return False, f"Flash failed: {error_msg}"
        
        except Exception as e:
            return False, f"Error during flash operation: {e}"
    
    def stop_current_operation(self):
        """Stop the current commander operation"""
        self.should_stop = True
        if self.current_process:
            try:
                self.current_process.terminate()
                self.debug_log("Commander process terminated")
            except Exception as e:
                self.debug_log(f"Error terminating commander process: {e}")
    
    def get_device_info(self, j_link_serial=None):
        """Get connected device information"""
        if not self.validate_commander_path():
            return None
        
        try:
            cmd = [self.commander_path, "device", "info"]
            
            if j_link_serial:
                cmd.extend(["--serialno", j_link_serial])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return result.stdout
            else:
                self.debug_log(f"Error getting device info: {result.stderr}")
                return None
        
        except Exception as e:
            self.debug_log(f"Error running device info command: {e}")
            return None
    
    def reset_device(self, j_link_serial=None):
        """Reset the connected device"""
        if not self.validate_commander_path():
            return False, "Commander not available"
        
        try:
            cmd = [self.commander_path, "device", "reset"]
            
            if j_link_serial:
                cmd.extend(["--serialno", j_link_serial])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return True, "Device reset successfully"
            else:
                return False, f"Reset failed: {result.stderr}"
        
        except Exception as e:
            return False, f"Error during reset: {e}"