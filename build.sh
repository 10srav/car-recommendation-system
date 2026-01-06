#!/usr/bin/env bash
# Render build script for MyCar

set -o errexit

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install production server
pip install gunicorn

# Create necessary directories
mkdir -p logs static/uploads

echo "Build completed successfully!"
