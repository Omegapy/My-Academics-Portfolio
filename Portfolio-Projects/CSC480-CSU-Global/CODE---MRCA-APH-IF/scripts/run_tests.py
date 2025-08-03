#!/usr/bin/env python3
# -------------------------------------------------------------------------
# File: run_tests.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: scripts/run_tests.py
# -------------------------------------------------------------------------

# --- Module Objective ---
# Comprehensive test automation script for MRCA Advanced Parallel Hybrid system
# This script provides unified interface for running different test categories,
# generating coverage reports, and managing test execution across local development
# and CI/CD environments. Supports all test types including unit, integration,
# reliability, architecture, and end-to-end tests.
# -------------------------------------------------------------------------

# --- Module Contents Overview ---
# - Class: TestRunner - Main test execution coordinator
# - Class: TestConfig - Configuration management for test runs
# - Functions: CLI interface for test category selection and reporting
# - Functions: Coverage and reporting utilities
# -------------------------------------------------------------------------

# --- Dependencies / Imports ---
# - Standard Library:
#   - argparse: For command-line interface
#   - subprocess: For executing pytest commands
#   - pathlib: For file path management
#   - sys: For system interaction and exit codes
# - Third-Party: None (uses subprocess to call pytest)
# - Local Project Modules: None
# -------------------------------------------------------------------------

# --- Usage / Integration ---
# This script serves as the central testing interface for:
# - Local development testing workflows
# - CI/CD pipeline test execution
# - Coverage report generation
# - Test result aggregation and reporting
# Usage: python scripts/run_tests.py [test_category] [options]
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
MRCA Testing Automation Script

Unified interface for running comprehensive test suites across all categories
of the MRCA Advanced Parallel Hybrid system testing infrastructure.
"""

# =========================================================================
# Imports
# =========================================================================
# Standard library imports
import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

# =========================================================================
# Configuration Classes
# =========================================================================

# ------------------------------------------------------------------------- TestConfig
@dataclass
class TestConfig:
    """Configuration for test execution."""
    verbose: bool = True
    coverage: bool = True
    junit_xml: bool = True
    fail_fast: bool = False
    max_failures: int = 10
    timeout: int = 240  # 240 seconds default for LLM calls
    parallel: bool = False
    markers: List[str] = field(default_factory=list)
    output_dir: str = "test-results"
# ------------------------------------------------------------------------- end TestConfig

# ------------------------------------------------------------------------- TestResult
@dataclass 
class TestResult:
    """Results from test execution."""
    category: str
    success: bool
    exit_code: int
    duration: float
    test_count: int = 0
    passed_count: int = 0
    failed_count: int = 0
    output_file: Optional[str] = None
# ------------------------------------------------------------------------- end TestResult

# =========================================================================
# Test Runner Class
# =========================================================================

# ------------------------------------------------------------------------- TestRunner
class TestRunner:
    """Main test execution coordinator."""
    
    # ------------------------------------------------------------------------- __init__()
    def __init__(self, config: TestConfig):
        """Initialize test runner with configuration.
        
        Args:
            config: TestConfig instance with execution parameters
        """
        self.config = config
        self.project_root = Path(__file__).parent.parent
        self.test_results: List[TestResult] = []
        
        # Test category definitions
        self.test_categories = {
            "unit": {
                "path": "tests/unit/",
                "description": "Unit tests for individual components",
                "markers": ["unit"],
                "timeout": 240
            },
            "integration": {
                "path": "tests/integration/",
                "description": "Integration tests for Module 6 test cases",
                "markers": ["integration"],
                "timeout": 240
            },
            "reliability": {
                "path": "tests/reliability/",
                "description": "Reliability and fault injection tests",
                "markers": ["reliability"],
                "timeout": 240
            },
            "architecture": {
                "path": "tests/architecture/",
                "description": "Architecture and confidence tests",
                "markers": ["architecture"],
                "timeout": 240
            },
            "e2e": {
                "path": "tests/e2e/",
                "description": "End-to-end workflow tests",
                "markers": ["e2e", "requires_api"],
                "timeout": 240
            },
            "fast": {
                "path": "tests/unit/ tests/integration/",
                "description": "Fast test suite (unit + basic integration)",
                "markers": ["not slow"],
                "timeout": 240
            },
            "all": {
                "path": "tests/",
                "description": "Complete test suite",
                "markers": [],
                "timeout": 240
            }
        }
    # ------------------------------------------------------------------------- end __init__()
    
    # ------------------------------------------------------------------------- build_pytest_command()
    def build_pytest_command(self, category: str) -> List[str]:
        """Build pytest command for specified category.
        
        Args:
            category: Test category to run
            
        Returns:
            List of command arguments for subprocess
        """
        if category not in self.test_categories:
            raise ValueError(f"Unknown test category: {category}")
        
        cat_config = self.test_categories[category]
        cmd = ["python", "-m", "pytest"]
        
        # Add test paths
        cmd.extend(cat_config["path"].split())
        
        # Add verbosity
        if self.config.verbose:
            cmd.append("-v")
        
        # Add coverage
        if self.config.coverage and category != "e2e":
            cmd.extend(["--cov=backend", "--cov-report=xml", "--cov-report=term-missing"])
            if len(self.test_results) > 0:  # Append coverage for subsequent runs
                cmd.append("--cov-append")
        
        # Add JUnit XML output
        if self.config.junit_xml:
            output_file = f"{self.config.output_dir}/test-results-{category}.xml"
            cmd.extend(["--junit-xml", output_file])
        
        # Add markers
        markers = cat_config["markers"] + self.config.markers
        if markers:
            marker_expr = " and ".join(markers)
            cmd.extend(["-m", marker_expr])
        
        # Add failure handling
        if self.config.fail_fast:
            cmd.append("-x")
        elif self.config.max_failures:
            cmd.extend(["--maxfail", str(self.config.max_failures)])
        
        # Add timeout
        timeout = cat_config.get("timeout", self.config.timeout)
        cmd.extend(["--timeout", str(timeout)])
        
        # Add parallel execution
        if self.config.parallel and category in ["unit", "integration"]:
            cmd.extend(["-n", "auto"])
        
        # Add short traceback
        cmd.append("--tb=short")
        
        return cmd
    # ------------------------------------------------------------------------- end build_pytest_command()
    
    # ------------------------------------------------------------------------- run_category()
    def run_category(self, category: str) -> TestResult:
        """Run tests for a specific category.
        
        Args:
            category: Test category to execute
            
        Returns:
            TestResult with execution details
        """
        print(f"\n{'='*60}")
        print(f"Running {category.upper()} Tests")
        print(f"{'='*60}")
        print(f"Description: {self.test_categories[category]['description']}")
        
        start_time = time.time()
        
        try:
            cmd = self.build_pytest_command(category)
            print(f"Command: {' '.join(cmd)}")
            print("-" * 60)
            
            # Ensure output directory exists
            Path(self.config.output_dir).mkdir(exist_ok=True)
            
            # Run the test command
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=False,  # Show output in real-time
                text=True
            )
            
            duration = time.time() - start_time
            success = result.returncode == 0
            
            # Create test result
            test_result = TestResult(
                category=category,
                success=success,
                exit_code=result.returncode,
                duration=duration,
                output_file=f"{self.config.output_dir}/test-results-{category}.xml" if self.config.junit_xml else None
            )
            
            # Print result summary
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"\n{'-'*60}")
            print(f"{category.upper()} Tests: {status}")
            print(f"Duration: {duration:.2f}s")
            print(f"Exit Code: {result.returncode}")
            
            return test_result
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ ERROR: Failed to run {category} tests: {e}")
            
            return TestResult(
                category=category,
                success=False,
                exit_code=-1,
                duration=duration
            )
    # ------------------------------------------------------------------------- end run_category()
    
    # ------------------------------------------------------------------------- run_categories()
    def run_categories(self, categories: List[str]) -> List[TestResult]:
        """Run multiple test categories.
        
        Args:
            categories: List of test categories to run
            
        Returns:
            List of TestResult objects
        """
        results = []
        
        for category in categories:
            if category not in self.test_categories:
                print(f"⚠️  Unknown test category: {category}")
                continue
                
            result = self.run_category(category)
            results.append(result)
            self.test_results.append(result)
            
            # Stop on failure if fail_fast is enabled
            if not result.success and self.config.fail_fast:
                print(f"\n🛑 Stopping execution due to {category} test failure")
                break
        
        return results
    # ------------------------------------------------------------------------- end run_categories()
    
    # ------------------------------------------------------------------------- generate_summary()
    def generate_summary(self, results: List[TestResult]) -> None:
        """Generate and display test summary.
        
        Args:
            results: List of TestResult objects to summarize
        """
        print(f"\n{'='*60}")
        print("TEST EXECUTION SUMMARY")
        print(f"{'='*60}")
        
        total_duration = sum(r.duration for r in results)
        passed_categories = [r for r in results if r.success]
        failed_categories = [r for r in results if not r.success]
        
        print(f"Total Categories: {len(results)}")
        print(f"Passed: {len(passed_categories)}")
        print(f"Failed: {len(failed_categories)}")
        print(f"Total Duration: {total_duration:.2f}s")
        print()
        
        # Detailed results
        for result in results:
            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"{status} {result.category:12} ({result.duration:6.2f}s)")
        
        print()
        
        # Coverage information
        if self.config.coverage:
            print("Coverage reports generated:")
            print("  - coverage.xml (for CI/CD)")
            print("  - Terminal output (above)")
            
        # JUnit XML information  
        if self.config.junit_xml:
            print("JUnit XML reports:")
            for result in results:
                if result.output_file:
                    print(f"  - {result.output_file}")
        
        print()
        
        # Final status
        if all(r.success for r in results):
            print("✅ ALL TESTS PASSED!")
            return True
        else:
            print("⚠️ SOME TESTS FAILED!")
            print("Check the output above for details.")
            return False
    # ------------------------------------------------------------------------- end generate_summary()
# ------------------------------------------------------------------------- end TestRunner

# =========================================================================
# CLI Interface Functions
# =========================================================================

# ------------------------------------------------------------------------- create_parser()
def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="MRCA Advanced Parallel Hybrid Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Test Categories:
  unit         - Unit tests for individual components
  integration  - Integration tests (Module 6 test cases)
  reliability  - Reliability and fault injection tests  
  architecture - Architecture and confidence tests
  e2e          - End-to-end workflow tests
  fast         - Fast test suite (unit + basic integration)
  all          - Complete test suite

Examples:
  python scripts/run_tests.py unit
  python scripts/run_tests.py fast --no-coverage
  python scripts/run_tests.py all --parallel --max-failures 5
  python scripts/run_tests.py unit integration reliability
        """
    )
    
    # Positional arguments
    parser.add_argument(
        "categories",
        nargs="+",
        help="Test categories to run (see categories above)"
    )
    
    # Optional arguments
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Disable coverage reporting"
    )
    
    parser.add_argument(
        "--no-junit",
        action="store_true", 
        help="Disable JUnit XML output"
    )
    
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce verbosity"
    )
    
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first failure"
    )
    
    parser.add_argument(
        "--max-failures",
        type=int,
        default=10,
        help="Maximum number of failures before stopping (default: 10)"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel (where supported)"
    )
    
    parser.add_argument(
        "--output-dir",
        default="test-results",
        help="Output directory for test results (default: test-results)"
    )
    
    parser.add_argument(
        "--markers",
        nargs="*",
        default=[],
        help="Additional pytest markers to apply"
    )
    
    return parser
# ------------------------------------------------------------------------- end create_parser()

# ------------------------------------------------------------------------- main()
def main() -> int:
    """Main entry point for test runner.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # Create test configuration
    config = TestConfig(
        verbose=not args.quiet,
        coverage=not args.no_coverage,
        junit_xml=not args.no_junit,
        fail_fast=args.fail_fast,
        max_failures=args.max_failures,
        parallel=args.parallel,
        markers=args.markers,
        output_dir=args.output_dir
    )
    
    # Create test runner
    runner = TestRunner(config)
    
    # Validate categories
    valid_categories = set(runner.test_categories.keys())
    invalid_categories = set(args.categories) - valid_categories
    
    if invalid_categories:
        print(f"❌ Invalid test categories: {', '.join(invalid_categories)}")
        print(f"Valid categories: {', '.join(sorted(valid_categories))}")
        return 1
    
    # Run tests
    print("MRCA Advanced Parallel Hybrid Test Runner")
    print(f"Categories: {', '.join(args.categories)}")
    print(f"Configuration: {config}")
    
    results = runner.run_categories(args.categories)
    success = runner.generate_summary(results)
    
    return 0 if success else 1
# ------------------------------------------------------------------------- end main()

# =========================================================================
# Entry Point
# =========================================================================

if __name__ == "__main__":
    sys.exit(main())

# =========================================================================
# End of File
# ========================================================================= 