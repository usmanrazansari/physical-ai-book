#!/bin/bash
# Setup script for Physical AI Book Backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install playwright and its dependencies
playwright install

echo "Setup complete! To activate the environment, run: source venv/bin/activate"