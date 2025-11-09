#!/bin/bash
# Setup script for Taiwan OT Job Search Monitor

set -e

echo "========================================"
echo "Taiwan OT Job Search Monitor - Setup"
echo "========================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
playwright install

# Create data directory
mkdir -p data

# Check for .env file
echo ""
if [ ! -f ".env" ]; then
    echo "⚠️  Configuration file .env not found"
    echo "   Copying from .env.example..."
    cp .env.example .env
    echo ""
    echo "   Please edit .env and add your Telegram credentials:"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - TELEGRAM_CHAT_ID"
else
    echo "✓ Configuration file .env already exists"
fi

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Telegram credentials"
echo "2. Run: python test_scraper.py (to test the scraper)"
echo "3. Run: python main.py (to start the job monitor)"
echo ""
