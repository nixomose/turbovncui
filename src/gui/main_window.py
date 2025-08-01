from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox,
    QLabel
)
from PyQt6.QtCore import Qt
from utils.database import ConnectionDatabase
from utils.vnc_launcher import VNCLaucher
from gui.connection_dialog import ConnectionDialog


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.db = ConnectionDatabase()
        self.vnc_launcher = VNCLaucher()
        self.connections = []
        self.last_connection = None
        
        self.setup_ui()
        self.load_connections()
        self.load_last_connection()
    
    def setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("TurboVNC UI")
        self.setMinimumSize(600, 400)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("TurboVNC Connection Manager")
        title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; margin: 10px;"
        )
        layout.addWidget(title_label)
        
        # Connection list
        self.connection_list = QListWidget()
        self.connection_list.itemDoubleClicked.connect(self.edit_connection)
        layout.addWidget(self.connection_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Add button
        self.add_button = QPushButton("Add Connection")
        self.add_button.clicked.connect(self.add_connection)
        button_layout.addWidget(self.add_button)
        
        # Edit button
        self.edit_button = QPushButton("Edit Connection")
        self.edit_button.clicked.connect(self.edit_selected_connection)
        button_layout.addWidget(self.edit_button)
        
        # Delete button
        self.delete_button = QPushButton("Delete Connection")
        self.delete_button.clicked.connect(self.delete_selected_connection)
        button_layout.addWidget(self.delete_button)
        
        # Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_selected)
        self.connect_button.setStyleSheet(
            "background-color: #4CAF50; color: white;"
        )
        button_layout.addWidget(self.connect_button)
        
        layout.addLayout(button_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def load_connections(self):
        """Load connections from database."""
        self.connections = self.db.load_connections()
        self.update_connection_list()
    
    def load_last_connection(self):
        """Load and highlight the last used connection."""
        self.last_connection = self.db.load_last_connection()
        if self.last_connection:
            # Find and select the last connection in the list
            for i in range(self.connection_list.count()):
                item = self.connection_list.item(i)
                if (item.data(Qt.ItemDataRole.UserRole) == 
                    self.last_connection.name):
                    self.connection_list.setCurrentItem(item)
                    break
    
    def update_connection_list(self):
        """Update the connection list display."""
        self.connection_list.clear()
        
        for connection in self.connections:
            item = QListWidgetItem(str(connection))
            item.setData(Qt.ItemDataRole.UserRole, connection.name)
            self.connection_list.addItem(item)
    
    def add_connection(self):
        """Add a new connection."""
        dialog = ConnectionDialog(self)
        if dialog.exec() == ConnectionDialog.DialogCode.Accepted:
            connection, _ = dialog.get_connection_data()
            
            # Check if name already exists
            if any(c.name == connection.name for c in self.connections):
                QMessageBox.warning(
                    self, "Error", 
                    "A connection with this name already exists!"
                )
                return
            
            self.db.add_connection(connection)
            self.load_connections()
            self.statusBar().showMessage(f"Added connection: {connection.name}")
    
    def edit_selected_connection(self):
        """Edit the selected connection."""
        current_item = self.connection_list.currentItem()
        if not current_item:
            QMessageBox.information(
                self, "Info", 
                "Please select a connection to edit."
            )
            return
        
        connection_name = current_item.data(Qt.ItemDataRole.UserRole)
        connection = self.db.get_connection_by_name(connection_name)
        
        if connection:
            self.edit_connection(current_item)
    
    def edit_connection(self, item):
        """Edit a connection."""
        connection_name = item.data(Qt.ItemDataRole.UserRole)
        connection = self.db.get_connection_by_name(connection_name)
        
        if not connection:
            return
        
        dialog = ConnectionDialog(self, connection)
        if dialog.exec() == ConnectionDialog.DialogCode.Accepted:
            new_connection, old_name = dialog.get_connection_data()
            
            # Check if new name conflicts with existing connections
            if (new_connection.name != old_name and 
                any(c.name == new_connection.name for c in self.connections)):
                QMessageBox.warning(
                    self, "Error", 
                    "A connection with this name already exists!"
                )
                return
            
            self.db.update_connection(old_name, new_connection)
            self.load_connections()
            self.statusBar().showMessage(f"Updated connection: {new_connection.name}")
    
    def delete_selected_connection(self):
        """Delete the selected connection."""
        current_item = self.connection_list.currentItem()
        if not current_item:
            QMessageBox.information(
                self, "Info", 
                "Please select a connection to delete."
            )
            return
        
        connection_name = current_item.data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{connection_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_connection(connection_name):
                self.load_connections()
                self.statusBar().showMessage(f"Deleted connection: {connection_name}")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete connection.")
    
    def connect_to_selected(self):
        """Connect to the selected VNC server."""
        current_item = self.connection_list.currentItem()
        if not current_item:
            QMessageBox.information(
                self, "Info", 
                "Please select a connection to connect to."
            )
            return
        
        connection_name = current_item.data(Qt.ItemDataRole.UserRole)
        connection = self.db.get_connection_by_name(connection_name)
        
        if not connection:
            QMessageBox.warning(self, "Error", "Connection not found.")
            return
        
        # Save as last used connection
        self.db.save_last_connection(connection)
        
        # Launch TurboVNC
        if self.vnc_launcher.launch_connection(connection):
            self.statusBar().showMessage(f"Connecting to {connection.name}...")
        else:
            QMessageBox.critical(
                self, "Error", 
                "Failed to launch TurboVNC. Please check your installation."
            ) 