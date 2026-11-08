#!/bin/bash
# This script runs after pip install requirements.txt
# It downloads the spaCy model to the container

echo "🔧 Installing spaCy language model..."
python -m spacy download en_core_web_sm

echo "✅ Setup complete!"
