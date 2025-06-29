#!/bin/bash

# This script is run by Vercel during the build process.

# Exit immediately if a command exits with a non-zero status.
set -ex

echo "=== RUNNING BUILDSH ==="

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

# 5. Create the function's specific config file
echo "Creating function config..."
cat > .vercel/output/functions/api/.vc-config.json <<EOF
{
  "runtime": "python3.12",
  "handler": "index.app",
  "launcherType": "FastApi"
}
EOF

# 6. Set the Playwright browser cache path to a location outside the function bundle
export PLAYWRIGHT_BROWSERS_PATH="/tmp/pw-browser-cache"

# 7. Install Playwright browser
pip install playwright-core
playwright install chromium

# 8. Move browser binaries to output directory
mkdir -p .vercel/output/_browser/
cp -r $PLAYWRIGHT_BROWSERS_PATH/* .vercel/output/_browser/ || true

# 9. Create the required config.json for Vercel Output File System
echo "=== ABOUT TO WRITE CONFIG.JSON ==="
cat > .vercel/output/config.json <<EOF
{
  "version": 3,
  "routes": [
    { "src": "/api/.*", "dest": "/functions/api/index.py" },
    { "src": "/(.*)", "dest": "/static/$1" }
  ]
}
EOF

echo "=== CONFIG.JSON CONTENTS ==="
ls -l .vercel/output/
cat .vercel/output/config.json

echo "Build script finished successfully." 