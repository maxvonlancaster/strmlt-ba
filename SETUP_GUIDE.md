# 🚀 Setup & Installation Guide

## Business Requirement Ticket Generator

This guide will walk you through setting up and running the Business Requirement Ticket Generator application.

## Quick Start (Recommended)

### Windows Users
1. Open Command Prompt or PowerShell in the `src/apps/` directory
2. Run: `quickstart.bat`
3. Wait for the application to start (it will open in your browser)

### Mac/Linux Users
1. Open Terminal in the `src/apps/` directory
2. Run: `bash quickstart.sh`
3. Wait for the application to start (it will open in your browser)

## Manual Installation

### Step 1: Prerequisites
Ensure you have:
- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (usually comes with Python)
- **git** (for version control)

Verify your Python installation:
```bash
python --version
pip --version
```

### Step 2: Navigate to the Application Directory
```bash
cd src/apps
```

### Step 3: Create a Virtual Environment (Recommended)

A virtual environment keeps project dependencies isolated.

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate.bat
```

#### Mac/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt when activated.

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install streamlit spacy plotly pandas scikit-learn
```

**Expected time**: 2-5 minutes depending on internet speed

### Step 5: Download spaCy Language Model

The application uses a spaCy language model for natural language processing.

```bash
python -m spacy download en_core_web_sm
```

**Expected time**: 1-2 minutes

### Step 6: Verify Installation

```bash
python -c "import streamlit; import spacy; print('✓ All dependencies installed successfully')"
```

If you see the success message, you're ready to run the app!

### Step 7: Run the Application

```bash
streamlit run requirement_ticket.py
```

The application should automatically open in your default browser at `http://localhost:8501`

If it doesn't open automatically, manually navigate to: **http://localhost:8501**

## Troubleshooting Installation

### Issue: "Python is not recognized"
**Solution**: Python is not in your PATH. Either:
1. Add Python to your PATH environment variable
2. Use the full path to Python: `C:\Python311\python.exe -m venv venv` (Windows)
3. Reinstall Python and check "Add Python to PATH" during installation

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Ensure you've installed the dependencies and your virtual environment is activated
```bash
pip install streamlit spacy plotly pandas scikit-learn
```

### Issue: "Error loading spaCy model"
**Solution**: Download the model again
```bash
python -m spacy download en_core_web_sm --force-all
```

### Issue: "Permission denied" on Mac/Linux
**Solution**: Make the quickstart script executable
```bash
chmod +x quickstart.sh
./quickstart.sh
```

### Issue: "Port 8501 is already in use"
**Solution**: Run on a different port
```bash
streamlit run requirement_ticket.py --server.port 8502
```

### Issue: Slow performance on first run
**Explanation**: The application loads the spaCy model on first startup, which takes 30-60 seconds. Subsequent runs are much faster.

## System Requirements

### Minimum Requirements
- **OS**: Windows 7+, macOS 10.9+, or Linux
- **RAM**: 2 GB (4 GB recommended)
- **Disk Space**: 500 MB (for dependencies and spaCy model)
- **Python**: 3.8 or higher

### Recommended Requirements
- **RAM**: 4-8 GB
- **SSD**: For faster model loading
- **Modern Browser**: Chrome, Firefox, Safari, or Edge

## Optional: Enhanced Setup

### For Better NLP Performance
Install the larger spaCy model:
```bash
python -m spacy download en_core_web_md
```

Then modify `requirement_processor.py` line 89:
```python
self.nlp = spacy.load("en_core_web_md")  # Instead of "en_core_web_sm"
```

### For Sentence Vector Support
Install sentence transformers (used in the original ba.ipynb):
```bash
pip install sentence-transformers
```

### For GPU Support (Advanced)
If you have an NVIDIA GPU:
```bash
pip install spacy-gpu
python -m spacy download en_core_web_sm --gpu
```

## Verifying Your Installation

Create a test file `test_setup.py` with:
```python
import streamlit
import spacy
import plotly
import pandas
from requirement_processor import RequirementProcessor

print("✓ Streamlit:", streamlit.__version__)
print("✓ spaCy:", spacy.__version__)
print("✓ Plotly:", plotly.__version__)
print("✓ Pandas:", pandas.__version__)
print("✓ RequirementProcessor: Loaded successfully")

# Test the processor
processor = RequirementProcessor()
result = processor.extract_entities("We need a mobile app for users")
print("✓ Entity extraction working:", result['stakeholder'], result['action'])
print("\n✅ All systems operational!")
```

Run it:
```bash
python test_setup.py
```

## Running the Application

### Start the Application
```bash
streamlit run requirement_ticket.py
```

### Stop the Application
Press `Ctrl+C` in the terminal where the application is running

### Access the Application
- **Local**: http://localhost:8501
- **Network**: http://<your-ip-address>:8501
  - Find your IP address:
	- Windows: `ipconfig`
	- Mac/Linux: `ifconfig`

## Deployment Options

### Local Testing
```bash
streamlit run requirement_ticket.py
```

### Share Temporarily
```bash
streamlit run requirement_ticket.py --logger.level=error --client.showErrorDetails=false
```

Then share the URL printed to the console.

### Deploy to Streamlit Cloud (Free)
1. Push your code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your GitHub repository and branch
5. Set the main file path to `src/apps/requirement_ticket.py`
6. Deploy!

### Deploy Locally (Production)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 1 --timeout 120 -b 0.0.0.0:8501 streamlit.web.bootstrap:run_app requirement_ticket
```

## Environment Variables

You can configure the application via environment variables:

```bash
# Set the spaCy model to use
export SPACY_MODEL=en_core_web_md

# Set Streamlit configuration
export STREAMLIT_SERVER_PORT=8502
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
```

## Maintenance

### Update Dependencies
```bash
pip install --upgrade streamlit spacy plotly pandas scikit-learn
python -m spacy download en_core_web_sm
```

### Clean Up
```bash
# Remove virtual environment (safe to delete)
rm -rf venv

# Clear spaCy cache
python -m spacy info --exclude models
```

## Performance Optimization

### Cache Management
The application automatically caches the spaCy processor. To clear cache:
```bash
# Delete Streamlit cache
rm -rf ~/.streamlit/cache/

# On Windows: 
# Delete %APPDATA%\.streamlit\cache\
```

### Reduce Memory Usage
Edit `requirement_ticket.py` and remove the `@st.cache_resource` decorator if needed:
```python
# Before
@st.cache_resource
def load_processor():
	return RequirementProcessor()

# After (reloads on each run, more memory efficient)
def load_processor():
	return RequirementProcessor()
```

## Getting Help

1. **Check Requirements**: Ensure all dependencies are installed
   ```bash
   pip list | grep -E "streamlit|spacy|plotly|pandas"
   ```

2. **Check spaCy Model**: Verify the model is installed
   ```bash
   python -m spacy info en_core_web_sm
   ```

3. **Check Logs**: Run with verbose logging
   ```bash
   streamlit run requirement_ticket.py --logger.level=debug
   ```

4. **Test Individual Components**: Run `test_setup.py` (see Verification section)

5. **Online Resources**:
   - Streamlit Docs: https://docs.streamlit.io
   - spaCy Docs: https://spacy.io/
   - Plotly Docs: https://plotly.com/python/

## Next Steps

After successful installation:
1. Read [README_REQUIREMENT_TICKET.md](./README_REQUIREMENT_TICKET.md) for application usage
2. Explore the sidebar help section in the app
3. Try the built-in examples
4. Process your own business requirements
5. Export and analyze the generated tickets

---

**Troubleshooting Updated**: 2024
**Version**: 1.0
