#!/bin/bash

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies for Tailwind CSS
echo "Installing Node.js dependencies..."
npm install

# Build Tailwind CSS - only if input.css exists and is newer than output.css
if [ -f "./static/css/input.css" ]; then
    echo "Building Tailwind CSS..."
    npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify
fi

# Run Django migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"
