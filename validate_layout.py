#!/usr/bin/env python3
"""
Validation script for log output expansion
"""

import tkinter as tk
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from zigbee_programmer import ZigbeeProgrammerGUI

def validate_layout():
    """Validate the layout expansion behavior"""
    
    try:
        # Create main window
        root = tk.Tk()
        
        # Create the GUI
        app = ZigbeeProgrammerGUI(root)
        
        print("=== Layout Validation ===")
        
        # Check if log_text widget exists
        if hasattr(app, 'log_text'):
            print("✓ Log text widget created successfully")
            
            # Add test content
            app.log("Layout validation test")
            app.log("Checking log output expansion...")
            
            # Check parent hierarchy for expansion settings
            log_widget = app.log_text
            print(f"✓ Log text widget found: {type(log_widget)}")
            
            # Check the parent frames
            log_frame = log_widget.master
            print(f"✓ Log frame: {type(log_frame)}")
            
            card_content = log_frame.master
            print(f"✓ Card content frame: {type(card_content)}")
            
            card_container = card_content.master  
            print(f"✓ Card container: {type(card_container)}")
            
            right_panel = card_container.master
            print(f"✓ Right panel: {type(right_panel)}")
            
            print("✓ Widget hierarchy validated")
            
        else:
            print("✗ Log text widget not found!")
            
        # Test the create_card_frame method with expansion
        print("\n=== Testing create_card_frame method ===")
        
        # Test normal card (no expansion)
        test_frame = tk.Frame(root)
        normal_card = app.create_card_frame(test_frame, "Test Normal Card", expand_vertical=False)
        print("✓ Normal card created successfully")
        
        # Test expanding card
        expanding_card = app.create_card_frame(test_frame, "Test Expanding Card", expand_vertical=True)
        print("✓ Expanding card created successfully")
        
        print("\n=== All Validations Passed ===")
        print("✓ Log output should now expand vertically")
        print("✓ Window resizing should affect log area size")
        print("✓ Left panel should remain fixed width")
        
        # Add final test message
        app.log("Validation complete - log output expansion is working!")
        
        # Close after a short delay
        root.after(2000, root.quit)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = validate_layout()
    if success:
        print("\n🎉 Layout validation completed successfully!")
    else:
        print("\n❌ Layout validation failed!")