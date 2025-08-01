import json
import os
from pathlib import Path
from typing import List, Optional
from turbovncui.models.connection import Connection


class ConnectionDatabase:
    """Manages storage and retrieval of VNC connections."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize database with config directory."""
        if config_dir is None:
            config_dir = os.path.expanduser("~/.config/turbovncui")
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.connections_file = self.config_dir / "connections.json"
        self.last_connection_file = self.config_dir / "last_connection.json"
    
    def save_connections(self, connections: List[Connection]) -> None:
        """Save connections to JSON file."""
        data = [conn.to_dict() for conn in connections]
        with open(self.connections_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_connections(self) -> List[Connection]:
        """Load connections from JSON file."""
        if not self.connections_file.exists():
            return []
        
        try:
            with open(self.connections_file, 'r') as f:
                data = json.load(f)
            return [Connection.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, ValueError):
            # If file is corrupted, return empty list
            return []
    
    def save_last_connection(self, connection: Connection) -> None:
        """Save the last used connection."""
        data = connection.to_dict()
        with open(self.last_connection_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_last_connection(self) -> Optional[Connection]:
        """Load the last used connection."""
        if not self.last_connection_file.exists():
            return None
        
        try:
            with open(self.last_connection_file, 'r') as f:
                data = json.load(f)
            return Connection.from_dict(data)
        except (json.JSONDecodeError, KeyError, ValueError):
            return None
    
    def add_connection(self, connection: Connection) -> None:
        """Add a new connection."""
        connections = self.load_connections()
        connections.append(connection)
        self.save_connections(connections)
    
    def update_connection(self, old_name: str, new_connection: Connection) -> bool:
        """Update an existing connection."""
        connections = self.load_connections()
        for i, conn in enumerate(connections):
            if conn.name == old_name:
                connections[i] = new_connection
                self.save_connections(connections)
                return True
        return False
    
    def delete_connection(self, name: str) -> bool:
        """Delete a connection by name."""
        connections = self.load_connections()
        original_count = len(connections)
        connections = [
            conn for conn in connections
            if conn.name != name
        ]
        
        if len(connections) < original_count:
            self.save_connections(connections)
            return True
        return False
    
    def get_connection_by_name(self, name: str) -> Optional[Connection]:
        """Get a connection by name."""
        connections = self.load_connections()
        for conn in connections:
            if conn.name == name:
                return conn
        return None 