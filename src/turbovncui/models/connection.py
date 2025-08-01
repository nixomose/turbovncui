from dataclasses import dataclass
from typing import Optional


@dataclass
class Connection:
    """Represents a VNC server connection."""
    name: str
    host: str
    port: int = 5900
    username: Optional[str] = None
    display: Optional[str] = None
    
    def __post_init__(self):
        """Validate connection data after initialization."""
        if not self.name.strip():
            raise ValueError("Connection name cannot be empty")
        if not self.host.strip():
            raise ValueError("Host cannot be empty")
        if not (1 <= self.port <= 65535):
            raise ValueError("Port must be between 1 and 65535")
    
    def to_dict(self) -> dict:
        """Convert connection to dictionary for storage."""
        return {
            'name': self.name,
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'display': self.display
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Connection':
        """Create connection from dictionary."""
        return cls(
            name=data['name'],
            host=data['host'],
            port=data.get('port', 5900),
            username=data.get('username'),
            display=data.get('display')
        )
    
    def get_connection_string(self) -> str:
        """Get the connection string for TurboVNC."""
        if self.username:
            return f"{self.username}@{self.host}:{self.port}"
        else:
            return f"{self.host}:{self.port}"
    
    def __str__(self) -> str:
        """String representation for display."""
        if self.username:
            return f"{self.name} ({self.username}@{self.host}:{self.port})"
        else:
            return f"{self.name} ({self.host}:{self.port})" 