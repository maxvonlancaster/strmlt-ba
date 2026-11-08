#!/usr/bin/env bash
# Quick Start Script for Business Requirement Ticket Generator

echo "🚀 Business Requirement Ticket Generator - Quick Start"
echo "======================================================"
echo ""

# Check Python installation
echo "✓ Checking Python installation..."
python --version || { echo "❌ Python not found. Please install Python 3.8+"; exit 1; }
echo ""

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
	echo "📦 Creating virtual environment..."
	python -m venv venv

	# Activate virtual environment
	if [[ "$OSTYPE" == "win32" || "$OSTYPE" == "msys" ]]; then
		source venv/Scripts/activate
	else
		source venv/bin/activate
	fi
else
	echo "📦 Virtual environment already exists"
	if [[ "$OSTYPE" == "win32" || "$OSTYPE" == "msys" ]]; then
		source venv/Scripts/activate
	else
		source venv/bin/activate
	fi
fi
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install streamlit spacy plotly pandas scikit-learn
echo ""

# Download spaCy model
echo "⬇️  Downloading spaCy language model..."
python -m spacy download en_core_web_sm
echo ""

# Run the application
echo "✅ Setup complete!"
echo ""
echo "🎯 Starting the application..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
streamlit run requirement_ticket.py
