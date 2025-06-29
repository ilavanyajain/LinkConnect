# Use the official Python image
FROM python:3.12-slim

# Install system dependencies and Node.js
RUN apt-get update && \
    apt-get install -y curl wget gnupg build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium

# Copy the rest of the code
COPY . .

# Expose the port Render will use
ENV PORT 10000
EXPOSE 10000

# Start the app
CMD ["python", "api/index.py"] 