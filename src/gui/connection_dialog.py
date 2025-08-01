from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QPushButton, QMessageBox
)
from models.connection import Connection


class ConnectionDialog(QDialog):
    """Dialog for adding or editing VNC connections."""
    
    def __init__(self, parent=None, connection=None):
        """Initialize dialog with optional existing connection."""
        super().__init__(parent)
        self.connection = connection
        self.is_editing = connection is not None
        
        title = "Edit Connection" if self.is_editing else "Add Connection"
        self.setWindowTitle(title)
        self.setModal(True)
        self.setup_ui()
        
        if self.is_editing:
            self.load_connection()
    
    def setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()
        
        # Form layout for connection details
        form_layout = QFormLayout()
        
        # Connection name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter connection name")
        form_layout.addRow("Name:", self.name_edit)
        
        # Host
        self.host_edit = QLineEdit()
        self.host_edit.setPlaceholderText("Enter hostname or IP address")
        form_layout.addRow("Host:", self.host_edit)
        
        # Port
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.port_spin.setValue(5900)
        form_layout.addRow("Port:", self.port_spin)
        
        # Username
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter username (optional)")
        form_layout.addRow("Username:", self.username_edit)
        
        # Display
        self.display_edit = QLineEdit()
        self.display_edit.setPlaceholderText("Enter display (optional)")
        form_layout.addRow("Display:", self.display_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.save_button.setDefault(True)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Set reasonable size
        self.resize(400, 200)
    
    def load_connection(self):
        """Load existing connection data into the form."""
        if not self.connection:
            return
        
        self.name_edit.setText(self.connection.name)
        self.host_edit.setText(self.connection.host)
        self.port_spin.setValue(self.connection.port)
        
        if self.connection.username:
            self.username_edit.setText(self.connection.username)
        
        if self.connection.display:
            self.display_edit.setText(self.connection.display)
    
    def get_connection(self) -> Connection:
        """Get the connection from the form data."""
        name = self.name_edit.text().strip()
        host = self.host_edit.text().strip()
        port = self.port_spin.value()
        username = self.username_edit.text().strip() or None
        display = self.display_edit.text().strip() or None
        
        return Connection(
            name=name,
            host=host,
            port=port,
            username=username,
            display=display
        )
    
    def accept(self):
        """Validate and accept the dialog."""
        try:
            self.get_connection()
            super().accept()
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))
    
    def get_connection_data(self) -> tuple[Connection, str]:
        """Get connection data and old name (for editing)."""
        connection = self.get_connection()
        old_name = self.connection.name if self.is_editing else None
        return connection, old_name 