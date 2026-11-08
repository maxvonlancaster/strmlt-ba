@echo off
REM Quick Start Script for Business Requirement Ticket Generator (Windows)

echo.
echo 🚀 Business Requirement Ticket Generator - Quick Start
echo ======================================================
echo.

REM Check Python installation
echo ✓ Checking Python installation...
python --version >nul 2>&1 || (
	echo ❌ Python not found. Please install Python 3.8+ from https://www.python.org
	pause
	exit /b 1
)
python --version
echo.

REM Create virtual environment
if not exist "venv" (
	echo 📦 Creating virtual environment...
	python -m venv venv
) else (
	echo 📦 Virtual environment already exists
)
echo.

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo 📥 Installing dependencies...
pip install streamlit spacy plotly pandas scikit-learn
echo.

REM Download spaCy model
echo ⬇️  Downloading spaCy language model...
python -m spacy download en_core_web_sm
echo.

REM Run the application
echo ✅ Setup complete!
echo.
echo 🎯 Starting the application...
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
streamlit run requirement_ticket.py
pause
