#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "===> Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "===> Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "===> Build completed successfully!"
