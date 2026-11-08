#!/usr/bin/env python
"""
Setup script to download spaCy model on deployment
Run this before starting the app: python setup.py
"""

import subprocess
import sys

def download_spacy_model():
	"""Download spaCy model for Streamlit Cloud"""
	print("📥 Downloading spaCy model 'en_core_web_sm'...")
	try:
		subprocess.check_call(
			[sys.executable, "-m", "spacy", "download", "en_core_web_sm"],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		print("✅ spaCy model downloaded successfully!")
		return True
	except subprocess.CalledProcessError as e:
		print(f"⚠️  Warning: Could not download spaCy model: {e}")
		print("   The app will use a lightweight fallback model.")
		return False

if __name__ == "__main__":
	download_spacy_model()
