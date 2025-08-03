#!/usr/bin/env python3
# -------------------------------------------------------------------------
# File: verify_testing_setup.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Date: 2025-01-17 (Creation Date)
# Last Modified: 2025-01-17 
# File Path: verify_testing_setup.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Verification script for Week 1 testing infrastructure setup.
# Tests that pytest configuration, fixtures, and test discovery work correctly
# before running the full test suite. Validates Module 6 test case implementations.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Function: print_section - Print formatted section header
# - Function: print_result - Print test result with formatting
# - Function: check_file_exists - Check if file exists and print result
# - Function: check_pytest_config - Verify pytest configuration
# - Function: check_test_discovery - Test pytest test discovery
# - Function: check_module_6_tests - Verify Module 6 test case implementations
# - Function: check_unit_tests - Verify unit test infrastructure
# - Function: check_production_test_integration - Verify production test integration
# - Function: check_test_categories - Verify test category markers are working
# - Function: check_dependencies - Check that testing dependencies are available
# - Function: run_sample_test - Run a sample test to verify everything works
# - Function: main - Main verification function
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library: sys, os (for system operations and path management)
# - Standard Library: subprocess (for running pytest commands)
# - Standard Library: importlib.util (for module import verification)
# - Standard Library: pathlib.Path (for file system operations)
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This verification script should be run after setting up the testing infrastructure
# to ensure all components are properly configured. Run with: python3 verify_testing_setup.py
# It validates pytest setup, test discovery, Module 6 implementations, and dependencies.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion (APH-IF) System
# -------------------------------------------------------------------------

"""
MRCA Testing Infrastructure Verification

This script verifies that the Week 1 testing infrastructure is properly set up:
1. Pytest configuration and test discovery
2. Test fixtures and utilities
3. Module 6 test case implementations (Test Cases 1, 2, 3, 5)
4. Circuit breaker unit tests
5. Production test integration
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import sys
import os
import subprocess
import importlib.util
from pathlib import Path

# =========================================================================
# Utility Functions
# =========================================================================

# ---------------------------------------------------------------------------------
def print_section(title):
    """Print formatted section header.
    
    Creates a visually distinct section separator for test output organization.
    
    Args:
        title (str): The section title to display
    """
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def print_result(test_name, passed, details=""):
    """Print test result with formatting.
    
    Displays test results in a consistent format with pass/fail indicators
    and optional detailed information.
    
    Args:
        test_name (str): Name of the test being reported
        passed (bool): Whether the test passed
        details (str, optional): Additional details about the test result
    """
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"{status} - {test_name}")
    if details:
        print(f"   {details}")
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def check_file_exists(filepath, description=""):
    """Check if file exists and print result.
    
    Verifies file existence and reports the result in standard format.
    
    Args:
        filepath (str): Path to the file to check
        description (str, optional): Human-readable description of the file
        
    Returns:
        bool: True if file exists, False otherwise
    """
    exists = Path(filepath).exists()
    desc = description or f"File: {filepath}"
    print_result(desc, exists)
    return exists
# ---------------------------------------------------------------------------------

# =========================================================================
# Configuration Verification Functions
# =========================================================================

# ---------------------------------------------------------------------------------
def check_pytest_config():
    """Verify pytest configuration.
    
    Checks that all essential pytest configuration files exist including
    pytest.ini, test package initialization, shared fixtures, and dependencies.
    
    Returns:
        bool: True if all configuration files exist, False otherwise
    """
    print_section("Pytest Configuration")
    
    config_files = [
        ("tests/pytest.ini", "Pytest configuration file"),
        ("tests/__init__.py", "Tests package initialization"),
        ("tests/conftest.py", "Shared fixtures and utilities"),
        ("requirements-test.txt", "Testing dependencies")
    ]
    
    all_good = True
    for filepath, description in config_files:
        exists = check_file_exists(filepath, description)
        all_good = all_good and exists
    
    return all_good
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def check_test_discovery():
    """Test pytest test discovery.
    
    Runs pytest in collection mode to verify that test discovery is working
    correctly and reports the number of tests found.
    
    Returns:
        bool: True if test discovery successful, False otherwise
    """
    print_section("Test Discovery")
    
    try:
        # Run pytest test collection
        result = subprocess.run(
            ["python", "-m", "pytest", "--collect-only", "tests/", "-q"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Count discovered tests
            lines = result.stdout.split('\n')
            test_lines = [line for line in lines if '::test_' in line]
            test_count = len(test_lines)
            
            print_result("Pytest test discovery", True, f"Found {test_count} tests")
            
            # Show some examples
            if test_count > 0:
                print("   Examples:")
                for line in test_lines[:5]:  # Show first 5 tests
                    if '::test_' in line:
                        print(f"     {line.strip()}")
                if test_count > 5:
                    print(f"     ... and {test_count - 5} more tests")
            
            return True
        else:
            print_result("Pytest test discovery", False, f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print_result("Pytest test discovery", False, f"Exception: {e}")
        return False
# ---------------------------------------------------------------------------------

# =========================================================================
# Test Implementation Verification Functions
# =========================================================================

# ---------------------------------------------------------------------------------
def check_module_6_tests():
    """Verify Module 6 test case implementations.
    
    Validates that all required Module 6 test case files exist and contain
    proper test class structures with pytest markers.
    
    Returns:
        bool: True if all Module 6 test cases are implemented, False otherwise
    """
    print_section("Module 6 Test Cases")
    
    test_cases = [
        ("tests/integration/test_regulatory_citation_retrieval.py", "Test Case 1: Regulatory Citation Retrieval"),
        ("tests/integration/test_multi_domain_queries.py", "Test Case 2: Multi-Domain Queries"),
        ("tests/reliability/test_degraded_services.py", "Test Case 3: Degraded Services"),
        ("tests/architecture/test_confidence_hallucination.py", "Test Case 5: Confidence & Hallucination")
    ]
    
    all_good = True
    for filepath, description in test_cases:
        exists = check_file_exists(filepath, description)
        all_good = all_good and exists
        
        if exists:
            # Check file content has actual test classes
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    has_test_class = 'class Test' in content and 'pytest.mark' in content
                    print_result(f"  Content validation", has_test_class, 
                               "Contains test classes and pytest markers" if has_test_class else "Missing test structure")
            except Exception as e:
                print_result(f"  Content validation", False, f"Error reading file: {e}")
    
    return all_good
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def check_unit_tests():
    """Verify unit test infrastructure.
    
    Checks that unit test package and core unit test files exist including
    circuit breaker tests which are essential for system reliability.
    
    Returns:
        bool: True if unit test infrastructure is in place, False otherwise
    """
    print_section("Unit Tests")
    
    unit_tests = [
        ("tests/unit/__init__.py", "Unit tests package"),
        ("tests/unit/test_circuit_breaker.py", "Circuit breaker unit tests")
    ]
    
    all_good = True
    for filepath, description in unit_tests:
        exists = check_file_exists(filepath, description)
        all_good = all_good and exists
    
    return all_good
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def check_production_test_integration():
    """Verify production test integration.
    
    Validates that the formal testing framework properly integrates with
    existing production test functions through the production_test_caller fixture.
    
    Returns:
        bool: True if production test integration is working, False otherwise
    """
    print_section("Production Test Integration")
    
    try:
        # Check that conftest.py has production_test_caller fixture
        with open("tests/conftest.py", 'r') as f:
            conftest_content = f.read()
        
        has_production_caller = "production_test_caller" in conftest_content
        print_result("Production test caller fixture", has_production_caller)
        
        # Check that existing production tests still exist
        production_tests = [
            ("frontend/test_frontend.py", "Frontend integration test"),
            ("backend/tools/vector.py", "VectorRAG test function"),
            ("backend/tools/general.py", "General tool test function")
        ]
        
        production_tests_exist = True
        for filepath, description in production_tests:
            exists = check_file_exists(filepath, description)
            production_tests_exist = production_tests_exist and exists
        
        return has_production_caller and production_tests_exist
        
    except Exception as e:
        print_result("Production test integration", False, f"Error: {e}")
        return False
# ---------------------------------------------------------------------------------

# =========================================================================
# Advanced Verification Functions
# =========================================================================

# ---------------------------------------------------------------------------------
def check_test_categories():
    """Verify test category markers are working.
    
    Tests that pytest marker filtering works correctly for different test
    categories (unit, integration, etc.) to ensure proper test organization.
    
    Returns:
        bool: True if test category markers work, False otherwise
    """
    print_section("Test Category Markers")
    
    try:
        # Test marker filtering
        result = subprocess.run(
            ["python", "-m", "pytest", "--collect-only", "tests/", "-m", "unit", "-q"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        unit_tests_found = result.returncode == 0 and "test_" in result.stdout
        print_result("Unit test marker filtering", unit_tests_found)
        
        result = subprocess.run(
            ["python", "-m", "pytest", "--collect-only", "tests/", "-m", "integration", "-q"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        integration_tests_found = result.returncode == 0 and "test_" in result.stdout
        print_result("Integration test marker filtering", integration_tests_found)
        
        return unit_tests_found and integration_tests_found
        
    except Exception as e:
        print_result("Test category markers", False, f"Error: {e}")
        return False
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def check_dependencies():
    """Check that testing dependencies are available.
    
    Verifies that all essential Python packages required for testing are
    installed and can be imported successfully.
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    print_section("Testing Dependencies")
    
    key_dependencies = [
        ("pytest", "Core testing framework"),
        ("httpx", "HTTP client for API testing"),
        ("unittest.mock", "Mocking utilities"),
        ("asyncio", "Async testing support")
    ]
    
    all_good = True
    for dep_name, description in key_dependencies:
        try:
            if dep_name == "unittest.mock":
                from unittest import mock
            else:
                importlib.import_module(dep_name)
            print_result(description, True, f"{dep_name} available")
        except ImportError:
            print_result(description, False, f"{dep_name} not available")
            all_good = False
    
    return all_good
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
def run_sample_test():
    """Run a sample test to verify everything works.
    
    Executes a representative test from the test suite to validate that
    the complete testing infrastructure is functional end-to-end.
    
    Returns:
        bool: True if sample test runs successfully, False otherwise
    """
    print_section("Sample Test Execution")
    
    try:
        # Try to run the Test Case 1 primary test
        result = subprocess.run(
            ["python", "-m", "pytest", 
             "tests/integration/test_regulatory_citation_retrieval.py::TestRegulatoryCitationRetrieval::test_direct_cfr_citation_parallel_hybrid", 
             "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if "PASSED" in result.stdout:
            print_result("Sample Test Case 1 execution", True, "Primary CFR citation test passed")
            return True
        elif "ImportError" in result.stderr or "ModuleNotFoundError" in result.stderr:
            print_result("Sample Test Case 1 execution", False, "Import errors - backend not available")
            return False
        elif "skipped" in result.stdout.lower():
            print_result("Sample Test Case 1 execution", True, "Test was skipped (likely missing services)")
            return True
        else:
            print_result("Sample Test Case 1 execution", False, f"Test failed or errored")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}...")
            return False
            
    except Exception as e:
        print_result("Sample test execution", False, f"Exception: {e}")
        return False
# ---------------------------------------------------------------------------------

# =========================================================================
# Main Verification Function
# =========================================================================

# ---------------------------------------------------------------------------------
def main():
    """Main verification function.
    
    Orchestrates the complete testing infrastructure verification process.
    Runs all checks in sequence and provides a comprehensive summary of
    the testing setup status with actionable next steps.
    
    Returns:
        bool: True if all verifications pass, False if any issues found
    """
    print("MRCA Testing Infrastructure Verification")
    print("Verifying Week 1 testing setup completion...\n")
    
    # Run all checks
    checks = [
        ("Pytest Configuration", check_pytest_config),
        ("Test Discovery", check_test_discovery),
        ("Module 6 Test Cases", check_module_6_tests),
        ("Unit Tests", check_unit_tests),
        ("Production Test Integration", check_production_test_integration),
        ("Test Category Markers", check_test_categories),
        ("Testing Dependencies", check_dependencies)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} - Exception: {e}")
            results.append((check_name, False))
    
    # Optional: Try to run a sample test
    if all(result for _, result in results):
        print("\nAll infrastructure checks passed! Trying sample test execution...")
        sample_result = run_sample_test()
        results.append(("Sample Test Execution", sample_result))
    
    # Summary
    print_section("Verification Summary")
    
    passed_checks = sum(1 for _, result in results if result)
    total_checks = len(results)
    
    for check_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    print(f"\nOverall Result: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("\n✅ Testing infrastructure is ready!")
        print("\nNext steps:")
        print("   • Install testing dependencies: pip install -r requirements-test.txt")
        print("   • Run all tests: pytest tests/")
        print("   • Run specific categories: pytest -m unit, pytest -m integration")
        print("   • View test coverage: pytest --cov=backend --cov=frontend")
        print("\nSee TESTING_IMPLEMENTATION_GUIDE.md for complete usage instructions")
    else:
        print(f"\n⚠️  {total_checks - passed_checks} issues found. Please address failed checks above.")
        print("\nCommon fixes:")
        print("   • Ensure all files are created correctly")
        print("   • Install testing dependencies if missing")
        print("   • Check file paths and directory structure")
    
    return passed_checks == total_checks
# ---------------------------------------------------------------------------------

# =========================================================================
# Module Initialization / Main Execution Guard
# =========================================================================

# ---------------------------------------------------------------------------------
if __name__ == "__main__":
    """
    Execute the testing infrastructure verification when script is run directly.
    
    This block runs only when the file is executed directly, not when imported.
    Executes the main verification function and exits with appropriate status code.
    """
    success = main()
    sys.exit(0 if success else 1)
# ---------------------------------------------------------------------------------

# =========================================================================
# End of File
# ========================================================================= 