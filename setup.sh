#!/bin/bash
# Setup script for Piano Practice App

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To run the app:"
echo "  1. source venv/bin/activate"
echo "  2. python -m piano_practice.main"
echo ""
echo "To deactivate the virtual environment later:"
echo "  deactivate"
