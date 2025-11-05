#!/usr/bin/env python3
"""
Test runner for Zigbee Device Programmer
"""

import os
import sys
import subprocess
import time

def run_test(test_file):
    """Run a single test file and return the result"""
    print(f"\n{'='*60}")
    print(f"Running {test_file}")
    print('='*60)
    
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=os.path.join(os.path.dirname(__file__), 'tests'),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"[PASS] ({duration:.2f}s)")
            if result.stdout:
                print("Output:")
                print(result.stdout)
            return True
        else:
            print(f"[FAIL] ({duration:.2f}s)")
            print("Error Output:")
            print(result.stderr)
            if result.stdout:
                print("Standard Output:")
                print(result.stdout)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] (30s)")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    """Run all tests"""
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    # Get all test files
    test_files = []
    for filename in os.listdir(tests_dir):
        if filename.startswith('test_') and filename.endswith('.py'):
            test_files.append(filename)
    
    test_files.sort()
    
    print(f"Found {len(test_files)} test files")
    print("Starting test run...")
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        if run_test(test_file):
            passed += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    print(f"Total tests: {len(test_files)}")
    print(f"Passed: {passed} [PASS]")
    print(f"Failed: {failed} [FAIL]")
    
    if failed == 0:
        print("\n*** ALL TESTS PASSED! ***")
        return 0
    else:
        print(f"\n*** {failed} TESTS FAILED ***")
        return 1

if __name__ == "__main__":
    sys.exit(main())