#!/bin/bash

# Build script for TurboVNC UI Debian package
# This script creates a .deb file that can be installed on Debian/Ubuntu systems

set -e

echo "Building TurboVNC UI Debian package..."

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Check if debian directory exists
if [ ! -d "debian" ]; then
    echo "Error: debian/ directory not found. Please ensure all Debian packaging files are present."
    exit 1
fi

# Install build dependencies
echo "Installing build dependencies..."
sudo apt-get update
sudo apt-get install -y build-essential devscripts debhelper dh-python python3-all python3-setuptools

# Create dist directory
echo "Creating dist directory..."
mkdir -p dist

# Clean any previous builds
echo "Cleaning previous builds..."
rm -rf debian/turbovncui/
rm -f dist/turbovncui_*.deb

# Create a simple icon (placeholder - you can replace this with a real icon)
echo "Creating placeholder icon..."
mkdir -p debian/
if [ ! -f "debian/turbovncui.png" ]; then
    # Create a simple 256x256 PNG icon using ImageMagick if available
    if command -v convert >/dev/null 2>&1; then
        convert -size 256x256 xc:transparent -fill "#4CAF50" -draw "circle 128,128 128,64" -fill white -pointsize 48 -gravity center -annotate +0+0 "VNC" debian/turbovncui.png
    else
        echo "Warning: ImageMagick not found. Creating empty icon file."
        # Create an empty file as placeholder
        touch debian/turbovncui.png
    fi
fi

# Build the package
echo "Building Debian package..."
debuild -b -us -uc

# Move the built package to dist directory
echo "Moving package to dist directory..."
mv ../turbovncui_*.deb dist/

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "Package files created:"
    ls -la dist/turbovncui_*.deb
    echo ""
    echo "To install the package:"
    echo "sudo dpkg -i dist/turbovncui_*.deb"
    echo ""
    echo "If there are dependency issues, run:"
    echo "sudo apt-get install -f"
else
    echo ""
    echo "❌ Build failed!"
    echo "Check the error messages above for details."
    exit 1
fi 