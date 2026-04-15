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

# Setup Site configuration for allauth
echo "Configuring Site for allauth..."
python manage.py setup_site

# Load products data if database is empty
echo "Checking products database..."
python manage.py shell << 'EOF'
from products.models import Product
import os

if Product.objects.count() == 0 and os.path.exists('data/products.json'):
    print("No products found. Loading from data/products.json...")
    os.system('python manage.py loaddata data/products.json')
    print("✓ Products loaded successfully!")
else:
    print(f"✓ Products already exist: {Product.objects.count()} products")
EOF

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"
