#!/bin/bash

# This script is run by Vercel during the build process.

# Exit immediately if a command exits with a non-zero status.
set -e

# 1. Create the directory structure Vercel expects
mkdir -p .vercel/output/functions/api/
mkdir -p .vercel/output/static/

# 2. Copy the static frontend files
echo "Copying static files..."
cp -r public/* .vercel/output/static/

# 3. Install Python dependencies into a specific directory
echo "Installing Python dependencies..."
pip install -r requirements.txt -t .vercel/output/functions/api/

# 4. Copy the backend Python code
echo "Copying backend code..."
cp api/index.py .vercel/output/functions/api/
cp linkedin_bot.py .vercel/output/functions/api/

# 5. Set the Playwright browser cache path to a location outside the function bundle
export PLAYWRIGHT_BROWSERS_PATH="/tmp/pw-browsers"

# 6. Install the single Chromium browser
echo "Installing Playwright browser..."
playwright install --with-deps chromium

# 7. Copy the browser installation from the temp path to a new location inside the build output
# This makes it available at runtime without being part of the function bundle.
echo "Moving browser files..."
mkdir -p .vercel/output/browser
mv $PLAYWRIGHT_BROWSERS_PATH/* .vercel/output/browser/

echo "Build script finished successfully." 