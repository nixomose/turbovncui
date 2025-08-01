# Debian Package Building Guide

This guide explains how to build Debian packages (.deb files) for TurboVNC UI.

## Prerequisites

### Local Build Requirements
- Ubuntu/Debian system
- Build tools: `build-essential`, `devscripts`, `debhelper`
- Python packaging tools: `dh-python`, `python3-all`, `python3-setuptools`
- ImageMagick (for icon generation): `imagemagick`

### Install Build Dependencies
```bash
sudo apt-get update
sudo apt-get install -y build-essential devscripts debhelper dh-python python3-all python3-setuptools imagemagick
```

## Building Locally

### Quick Build
Use the provided build script:
```bash
./build_deb.sh
```

This script will:
1. Install build dependencies
2. Create a placeholder icon
3. Build the Debian package
4. Show installation instructions

### Manual Build
If you prefer to build manually:

```bash
# Clean previous builds
rm -rf debian/turbovncui/
rm -f ../turbovncui_*.deb

# Create icon (if not present)
convert -size 256x256 xc:transparent -fill "#4CAF50" -draw "circle 128,128 128,64" -fill white -pointsize 48 -gravity center -annotate +0+0 "VNC" debian/turbovncui.png

# Build the package
debuild -b -us -uc
```

## Installing the Package

After building, install the package:
```bash
# Install the package
sudo dpkg -i ../turbovncui_*.deb

# Fix any dependency issues
sudo apt-get install -f
```

## Package Contents

The Debian package installs:
- **Binary**: `/usr/bin/turbovncui`
- **Desktop file**: `/usr/share/applications/turbovncui.desktop`
- **Icon**: `/usr/share/icons/hicolor/256x256/apps/turbovncui.png`
- **Man page**: `/usr/share/man/man1/turbovncui.1.gz`
- **Python package**: `/usr/lib/python3/dist-packages/turbovncui/`

## Dependencies

The package depends on:
- `python3-pyqt6` - GUI framework
- `turbovnc` - VNC client (must be installed separately)

## GitHub Releases

### Automated Builds
When you create a GitHub release, the GitHub Actions workflow will:
1. Automatically build the Debian package
2. Attach the .deb file to the release
3. Make it available for download

### Creating a Release
1. Tag a new version: `git tag v1.0.0`
2. Push the tag: `git push origin v1.0.0`
3. Create a GitHub release with the same tag
4. The workflow will automatically build and attach the .deb file

### Manual Workflow Trigger
You can also trigger the build manually:
1. Go to Actions tab in GitHub
2. Select "Build Debian Package" workflow
3. Click "Run workflow"

## Customization

### Icon
Replace `debian/turbovncui.png` with your own 256x256 PNG icon.

### Desktop File
Edit `debian/turbovncui.desktop` to modify:
- Application name and description
- Categories
- Keywords

### Package Metadata
Edit `debian/control` to modify:
- Package description
- Dependencies
- Maintainer information

### Version
Update version in:
- `debian/changelog`
- `setup.py`
- `src/main.py` (if needed)

## Troubleshooting

### Build Failures
- Check that all build dependencies are installed
- Ensure you're in the project root directory
- Verify all debian/ files are present

### Installation Issues
- Run `sudo apt-get install -f` to fix dependency issues
- Check that TurboVNC is installed: `which vncviewer`

### Icon Issues
- Ensure ImageMagick is installed for icon generation
- The build script creates a placeholder icon if none exists

## Distribution

### Personal Repository
You can host your own Debian repository:
1. Build the package
2. Set up a web server
3. Create a `Packages` file
4. Add your repository to `/etc/apt/sources.list`

### PPA (Personal Package Archive)
For Ubuntu users, you can create a PPA:
1. Build the source package: `debuild -S -us -uc`
2. Upload to Launchpad PPA
3. Users can add your PPA to install the package

### Direct Distribution
- Upload the .deb file to your website
- Users can download and install with `sudo dpkg -i package.deb`
- Include installation instructions for dependencies

## Version Management

### Semantic Versioning
Use semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

### Changelog
Update `debian/changelog` with:
- Version number
- Changes made
- Date and maintainer

Example:
```
turbovncui (1.0.1-1) unstable; urgency=medium

  * Fix double-click connection issue
  * Add better error handling
  * Update dependencies

 -- Your Name <your.email@example.com>  Mon, 01 Aug 2024 10:00:00 +0000
``` 