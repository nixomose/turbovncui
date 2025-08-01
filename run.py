#!/usr/bin/env python3
"""
Simple launcher for TurboVNC UI
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from main import main
    main() 