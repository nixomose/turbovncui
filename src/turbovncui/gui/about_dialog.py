from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import turbovncui


class AboutDialog(QDialog):
    """About dialog showing version and project information."""

    def __init__(self, parent=None):
        """Initialize the about dialog."""
        super().__init__(parent)
        self.setWindowTitle("About TurboVNC UI")
        self.setModal(True)
        self.setFixedSize(500, 400)
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()

        # Title and version
        title_label = QLabel("TurboVNC UI")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel(f"Version {turbovncui.__version__}")
        version_font = QFont()
        version_font.setPointSize(12)
        version_label.setFont(version_font)
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Description
        desc_label = QLabel(
            "A modern, user-friendly graphical interface for managing and "
            "launching TurboVNC connections."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        # Features list
        features_text = QTextEdit()
        features_text.setReadOnly(True)
        features_text.setMaximumHeight(150)
        features_text.setPlainText(
            "Features:\n"
            "• Connection management (add, edit, delete)\n"
            "• Persistent storage of connection settings\n"
            "• One-click connection to VNC servers\n"
            "• Remembers last used connection\n"
            "• Modern PyQt5-based interface\n"
            "• Compatible with XFCE and other desktop environments\n"
            "• Automatic TurboVNC detection\n"
            "• Enhanced error handling and user feedback"
        )
        layout.addWidget(features_text)

        # Author and license
        author_label = QLabel(
            "Author: TurboVNC UI Developer <nixomose@gmail.com>"
        )
        author_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(author_label)

        license_label = QLabel("License: MIT License")
        license_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(license_label)

        # Close button
        button_layout = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_button.setDefault(True)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout) 