# TurboVNC UI

A modern, user-friendly graphical interface for managing and launching TurboVNC connections. This application provides an intuitive way to create, edit, delete, and connect to VNC servers without having to remember command-line syntax.

## Features

- **Connection Management**: Create, edit, and delete VNC server connections
- **Persistent Storage**: All connections are saved locally and persist between sessions
- **Last Used Memory**: Automatically remembers and highlights your last used connection
- **One-Click Connect**: Launch TurboVNC with a single click
- **Modern Interface**: Clean, responsive GUI built with PyQt6
- **XFCE Compatible**: Designed to work seamlessly with XFCE desktop environment

## Screenshots

The application provides a clean interface with:
- Connection list showing all saved servers
- Add/Edit/Delete buttons for connection management
- Prominent "Connect" button for launching VNC sessions
- Status bar showing current operations

## Installation

### Prerequisites

- Python 3.8 or higher
- TurboVNC installed on your system
- Linux with XFCE (or other desktop environment)

### Quick Start

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd turbovncui
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

### Alternative Installation

You can also install it as a package:
```bash
pip install -e .
turbovncui
```

## Usage

### Adding a Connection

1. Click "Add Connection" button
2. Fill in the connection details:
   - **Name**: A friendly name for the connection (e.g., "Work Server")
   - **Host**: The server hostname or IP address
   - **Port**: VNC port (default: 5900)
   - **Username**: Your username on the remote server (optional)
   - **Display**: Display number (optional)
3. Click "Save"

### Connecting to a Server

1. Select a connection from the list
2. Click the green "Connect" button
3. TurboVNC will launch with the selected connection

### Editing Connections

- Double-click any connection in the list to edit it
- Or select a connection and click "Edit Connection"

### Deleting Connections

1. Select a connection from the list
2. Click "Delete Connection"
3. Confirm the deletion

## Configuration

The application stores all data in `~/.config/turbovncui/`:
- `connections.json`: All saved connections
- `last_connection.json`: Your last used connection

## TurboVNC Integration

This application is designed to work with TurboVNC's command-line interface. It launches connections using the format:

```bash
vncviewer username@host:port
```

Make sure TurboVNC is installed and `vncviewer` is available in your PATH.

## Development

### Project Structure

```
turbovncui/
├── src/
│   ├── main.py              # Application entry point
│   ├── gui/
│   │   ├── main_window.py   # Main application window
│   │   └── connection_dialog.py  # Connection editing dialog
│   ├── models/
│   │   └── connection.py    # Connection data model
│   └── utils/
│       ├── database.py      # Data persistence
│       └── vnc_launcher.py # TurboVNC integration
├── requirements.txt         # Python dependencies
├── setup.py               # Package configuration
├── run.py                 # Simple launcher script
└── README.md              # This file
```

### Running in Development

```bash
# Install in development mode
pip install -e .

# Run the application
python run.py
```

## Troubleshooting

### TurboVNC Not Found

If you get an error about TurboVNC not being found:
1. Ensure TurboVNC is installed on your system
2. Verify `vncviewer` is in your PATH
3. Try running `vncviewer --help` in terminal to test

### GUI Not Displaying

If the GUI doesn't appear:
1. Ensure you have a display server running (X11/Wayland)
2. Check that PyQt6 is properly installed
3. Try running with `DISPLAY=:0 python run.py`

### Connection Issues

- Verify the server is running and accessible
- Check firewall settings
- Ensure the correct port is specified
- Verify username/hostname are correct

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is open source and available under the MIT License.

## Requirements

- Python 3.8+
- PyQt6
- TurboVNC installed on your system
- Linux with X11/Wayland support 