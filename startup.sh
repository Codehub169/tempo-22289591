#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Navigate to the backend directory and install dependencies
echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

# Download spaCy English model
echo "Downloading spaCy NLP model (en_core_web_sm)..."
python -m spacy download en_core_web_sm

# Navigate to the frontend directory
echo "Navigating to frontend directory..."
cd frontend

# Install frontend dependencies
echo "Installing frontend dependencies (npm install)..."
npm install

# Build the frontend application
echo "Building frontend application (npm run build)..."
npm run build

# Navigate back to the project root directory
echo "Navigating back to project root..."
cd ..

# Start the backend server
echo "Starting backend server on port 9000..."
python backend/app.py
