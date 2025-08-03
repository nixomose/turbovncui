import subprocess
import os
from typing import Optional
from turbovncui.models.connection import Connection


class VNCLaucher:
    """Handles launching TurboVNC connections."""
    
    def __init__(self, turbovnc_path: Optional[str] = None):
        """Initialize with optional custom TurboVNC path."""
        if turbovnc_path:
            self.turbovnc_path = turbovnc_path
        else:
            self.turbovnc_path = self._find_turbovnc_binary()
    
    def _find_turbovnc_binary(self) -> str:
        """Find the TurboVNC binary, checking common locations first."""
        # Check the common TurboVNC installation path
        turbovnc_path = "/opt/TurboVNC/bin/vncviewer"
        if os.path.exists(turbovnc_path) and os.access(turbovnc_path, os.X_OK):
            return turbovnc_path
        
        # Fall back to system PATH
        return "vncviewer"
    
    def launch_connection(self, connection: Connection) -> bool:
        """Launch TurboVNC with the specified connection."""
        try:
            # Build the command
            cmd = [self.turbovnc_path]
            
            # Add username parameter if specified
            if connection.username:
                cmd.extend(["-User", connection.username])
            
            # Add the connection string
            cmd.append(connection.get_connection_string())
            
            # Launch the process
            subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Don't wait for the process to complete
            # TurboVNC viewer will run independently
            return True
            
        except FileNotFoundError:
            print(f"Error: TurboVNC viewer not found at "
                  f"'{self.turbovnc_path}'")
            print("Please ensure TurboVNC is installed and in your PATH")
            return False
        except Exception as e:
            print(f"Error launching TurboVNC: {e}")
            return False
    
    def test_connection(self, connection: Connection) -> bool:
        """Test if TurboVNC can be launched (doesn't actually connect)."""
        try:
            # Just check if the command exists and produces output
            result = subprocess.run(
                [self.turbovnc_path, "--help"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # TurboVNC returns 1 but still works, so check for output instead
            return len(result.stdout) > 0 or len(result.stderr) > 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def is_turbovnc_available(self) -> bool:
        """Check if TurboVNC is available and executable."""
        try:
            # Just check if the command exists and produces output
            result = subprocess.run(
                [self.turbovnc_path, "--help"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # TurboVNC returns 1 but still works, so check for output instead
            return len(result.stdout) > 0 or len(result.stderr) > 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def get_turbovnc_version(self) -> Optional[str]:
        """Get TurboVNC version if available."""
        try:
            result = subprocess.run(
                [self.turbovnc_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
    
    def get_detected_path(self) -> str:
        """Get the detected TurboVNC binary path."""
        return self.turbovnc_path 