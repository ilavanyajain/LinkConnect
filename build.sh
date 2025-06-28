#!/bin/bash

# This script is run by Vercel during the build process.

# Exit immediately if a command exits with a non-zero status.
set -e

# Install the Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright's browser dependencies and the single Chromium browser.
# The '--with-deps' flag ensures that any necessary OS-level libraries are installed.
echo "Installing Playwright browser..."
playwright install --with-deps chromium

echo "Build script finished successfully." 