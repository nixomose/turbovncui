#!/usr/bin/env python3
"""
TurboVNC UI - A graphical frontend for TurboVNC
"""

import sys
from PyQt5.QtWidgets import QApplication
from turbovncui.gui.main_window import MainWindow


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("TurboVNC UI")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 