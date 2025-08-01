#!/usr/bin/env python3
"""
Simple launcher for TurboVNC UI
"""

import sys
from pathlib import Path

# Add src to Python path for development
src_path = Path(__file__).parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    try:
        # Try to import from the installed package first
        from turbovncui.main import main
    except ImportError:
        # Fall back to local development version
        from main import main
    main() 