#!/bin/bash

# Setup script for Simple Proxmox MCP

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Setting up Simple Proxmox MCP..."

# Make scripts executable
chmod +x "$SCRIPT_DIR/manage-server.sh"
chmod +x "$SCRIPT_DIR/server.py"
chmod +x "$SCRIPT_DIR/proxmox_api.py"

# Install required Python packages
echo "Installing required Python packages..."
pip install -r "$SCRIPT_DIR/requirements.txt"

echo "Setup complete!"
echo "You can now start the server with: ./manage-server.sh start"