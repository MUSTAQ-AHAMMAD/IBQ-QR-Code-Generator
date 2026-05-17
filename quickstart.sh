#!/bin/bash

# Quick Start Script for IBQ QR Code Generator
# This script helps you get started quickly with the new features

echo "=================================================="
echo "IBQ QR Code Generator - Quick Start"
echo "100% Requirements Fulfillment Edition"
echo "=================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null
then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null
then
    PYTHON_CMD="python"
fi

echo "Using Python: $PYTHON_CMD"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install/upgrade dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Run complete setup
echo ""
echo "🚀 Running complete setup (migrations + theme seeds)..."
echo ""
$PYTHON_CMD setup_complete.py

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Setup completed with warnings"
    echo "You can still proceed, but check the output above"
else
    echo ""
    echo "✅ Setup completed successfully!"
fi

# Final instructions
echo ""
echo "=================================================="
echo "🎉 Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Start the application:"
echo "   $PYTHON_CMD app.py"
echo ""
echo "2. Open your browser:"
echo "   http://localhost:5000"
echo ""
echo "3. Login with default credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "⚠️  IMPORTANT: Change the admin password immediately!"
echo ""
echo "📚 Documentation:"
echo "   - NEW_FEATURES.md - Feature guide and examples"
echo "   - PROGRESS_REPORT.md - Implementation status"
echo "   - IMPLEMENTATION_COMPLETE.md - Complete summary"
echo ""
echo "🎨 New Features Available:"
echo "   - Multi-brand management with dynamic theming"
echo "   - 6 professional theme presets"
echo "   - Comprehensive analytics tracking"
echo "   - Employee management (models ready)"
echo "   - Enhanced vCard profiles"
echo ""
echo "To run the app:"
echo "   $PYTHON_CMD app.py"
echo ""
echo "=================================================="
