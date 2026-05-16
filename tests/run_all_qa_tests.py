#!/usr/bin/env python3
"""
Master QA Test Runner
Runs all QA tests in sequence and generates comprehensive reports.
"""
import asyncio
import subprocess
import sys
import os
from datetime import datetime

REPORTS_DIR = "/home/runner/work/IBQ-QR-Code-Generator/IBQ-QR-Code-Generator/qa-reports"


def print_header(title):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def run_command(command, description):
    """Run a command and capture output."""
    print(f"Running: {description}")
    print(f"Command: {command}\n")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )

        if result.returncode == 0:
            print(f"✓ {description} completed successfully\n")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"✗ {description} failed with return code {result.returncode}\n")
            if result.stderr:
                print("Error output:")
                print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(f"✗ {description} timed out after 10 minutes\n")
        return False
    except Exception as e:
        print(f"✗ {description} failed with exception: {e}\n")
        return False


async def main():
    """Main test runner."""
    start_time = datetime.now()

    print_header("IBQ QR Code Generator - Master QA Test Runner")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Create reports directory
    os.makedirs(REPORTS_DIR, exist_ok=True)

    results = {}

    # Step 1: Run E2E Tests
    print_header("Step 1: End-to-End Testing")
    results["e2e_tests"] = run_command(
        "pytest tests/e2e/ -v --html=qa-reports/e2e-report.html --self-contained-html",
        "E2E Tests"
    )

    # Step 2: Capture Screenshots
    print_header("Step 2: Automated Screenshot Capture")
    results["screenshots"] = run_command(
        "python tests/automated_screenshots.py",
        "Screenshot Capture"
    )

    # Step 3: Run Accessibility Tests
    print_header("Step 3: Accessibility Testing")
    results["accessibility"] = run_command(
        "python tests/accessibility_testing.py",
        "Accessibility Tests"
    )

    # Step 4: Run Visual QA Tests
    print_header("Step 4: Visual QA Testing")
    results["visual_qa"] = run_command(
        "python tests/visual_qa_testing.py",
        "Visual QA Tests"
    )

    # Step 5: Generate Final Audit Report
    print_header("Step 5: Generate Final Launch Audit")
    results["audit_report"] = run_command(
        "python tests/generate_launch_audit.py",
        "Launch Audit Report Generation"
    )

    # Summary
    end_time = datetime.now()
    duration = end_time - start_time

    print_header("Test Execution Summary")
    print(f"Started:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}\n")

    print("Results:")
    for test_name, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {test_name.replace('_', ' ').title()}: {status}")

    print("\nReports Generated:")
    print(f"  - E2E Test Report: {REPORTS_DIR}/e2e-report.html")
    print(f"  - Accessibility Report: {REPORTS_DIR}/accessibility/accessibility_report.md")
    print(f"  - Visual QA Report: {REPORTS_DIR}/visual-qa-report.md")
    print(f"  - Final Launch Audit: {REPORTS_DIR}/final-launch-audit.md")
    print(f"  - Screenshots: {REPORTS_DIR}/screenshots/")

    print("\n" + "=" * 70)

    # Exit with appropriate code
    if all(results.values()):
        print("✓ All tests completed successfully!")
        print("=" * 70 + "\n")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Review the output above.")
        print("=" * 70 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
