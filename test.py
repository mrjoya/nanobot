#!/usr/bin/env python3
"""
Master test script for NanoBot.

This script provides a convenient way to run various test suites
with different configurations.

Usage:
    python test.py                # Run all tests
    python test.py unit           # Run only unit tests (no API calls)
    python test.py integration    # Run only integration tests (requires API)
    python test.py styles         # Run only style-related tests
    python test.py generator      # Run only generator-related tests
    python test.py bot            # Run only bot-related tests
"""

import argparse
import subprocess
import sys
import os


def run_tests(test_type=None):
    """Run tests of the specified type."""
    # Base pytest command
    cmd = ["pytest", "-v"]
    
    # Configure based on test type
    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])
    elif test_type == "styles":
        cmd.append("tests/test_styles.py")
    elif test_type == "generator":
        cmd.append("tests/test_generator.py")
    elif test_type == "bot":
        cmd.extend(["tests/test_generator.py::TestGenerator::test_natural_language_parsing",
                   "tests/test_generator.py::TestGenerator::test_extract_relevant_phrases"])
    elif test_type == "dry":
        cmd.extend(["tests/test_generator.py::TestGenerator::test_dry_run_variations"])
    
    # Run the tests
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return result.returncode


def main():
    """Parse arguments and run tests."""
    parser = argparse.ArgumentParser(description="Run NanoBot tests")
    parser.add_argument("test_type", nargs="?", choices=[
        "unit", "integration", "styles", "generator", "bot", "dry", "all"
    ], default="all", help="Type of tests to run")
    parser.add_argument("--skip-env-check", action="store_true", 
                       help="Skip checking for API key in environment")
    
    args = parser.parse_args()
    
    # Check for API key if running integration tests
    if not args.skip_env_check and args.test_type in ["integration", "all"]:
        if not os.environ.get("FAL_KEY"):
            # Check if .env file exists and load it
            if os.path.exists(".env"):
                with open(".env", "r") as f:
                    for line in f:
                        if line.startswith("FAL_KEY="):
                            key = line.strip().split("=", 1)[1]
                            if key and key != "your_api_key_here":
                                os.environ["FAL_KEY"] = key
                                break
            
            # After trying to load from .env, check again
            if not os.environ.get("FAL_KEY"):
                print("WARNING: FAL_KEY environment variable not set.")
                print("Integration tests will fail without an API key.")
                print("Set up your API key in .env file or export it as an environment variable.")
                choice = input("Continue anyway? (y/n): ")
                if choice.lower() != "y":
                    print("Exiting.")
                    return 1
    
    # Run the tests
    return run_tests(args.test_type)


if __name__ == "__main__":
    sys.exit(main())