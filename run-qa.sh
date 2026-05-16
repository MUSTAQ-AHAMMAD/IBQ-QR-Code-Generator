#!/bin/bash
# Quick Start Script for QA Testing
# Usage: ./run-qa.sh

set -e

echo "======================================================================"
echo "  IBQ QR Code Generator - QA Testing Quick Start"
echo "======================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt
pip install -q -r requirements-qa.txt

# Install Playwright browsers
echo "✓ Installing Playwright browsers..."
playwright install chromium --quiet || playwright install chromium

# Create directories
echo "✓ Creating QA directories..."
mkdir -p qa-reports/{screenshots,errors,performance,accessibility}
mkdir -p uploads logs

# Check if application is running
echo ""
echo "Checking if application is running on port 5000..."
if ! curl -s http://127.0.0.1:5000/ > /dev/null; then
    echo ""
    echo "⚠️  Application is not running!"
    echo ""
    echo "Please start the application in another terminal:"
    echo "    python app.py"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "✓ Application is running"
echo ""

# Menu
echo "======================================================================"
echo "  Select Test Suite to Run"
echo "======================================================================"
echo ""
echo "  1) Run ALL tests (E2E + Screenshots + Accessibility + Visual QA)"
echo "  2) Run E2E tests only"
echo "  3) Capture screenshots only"
echo "  4) Run accessibility tests only"
echo "  5) Run visual QA tests only"
echo "  6) Generate launch audit only"
echo "  7) Exit"
echo ""
read -p "Enter choice [1-7]: " choice

case $choice in
    1)
        echo ""
        echo "Running all QA tests..."
        python tests/run_all_qa_tests.py
        ;;
    2)
        echo ""
        echo "Running E2E tests..."
        pytest tests/e2e/ -v --html=qa-reports/e2e-report.html --self-contained-html
        ;;
    3)
        echo ""
        echo "Capturing screenshots..."
        python tests/automated_screenshots.py
        ;;
    4)
        echo ""
        echo "Running accessibility tests..."
        python tests/accessibility_testing.py
        ;;
    5)
        echo ""
        echo "Running visual QA tests..."
        python tests/visual_qa_testing.py
        ;;
    6)
        echo ""
        echo "Generating launch audit..."
        python tests/generate_launch_audit.py
        ;;
    7)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac

echo ""
echo "======================================================================"
echo "✓ Testing Complete!"
echo "======================================================================"
echo ""
echo "Reports are available in: qa-reports/"
echo ""
echo "View reports:"
echo "  - E2E Report:       qa-reports/e2e-report.html"
echo "  - Screenshots:      qa-reports/screenshots/"
echo "  - Accessibility:    qa-reports/accessibility/accessibility_report.md"
echo "  - Visual QA:        qa-reports/visual-qa-report.md"
echo "  - Launch Audit:     qa-reports/final-launch-audit.md"
echo ""
echo "======================================================================"
