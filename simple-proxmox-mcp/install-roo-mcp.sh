#!/bin/bash

# Script to install the Simple Proxmox MCP server for Roo Code
# This script will copy the necessary files to the Roo Code MCP configuration directory

# Default Roo Code MCP configuration directory
DEFAULT_MCP_DIR="$HOME/.config/roo/mcp"

# Function to display usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Install the Simple Proxmox MCP server for Roo Code"
    echo ""
    echo "Options:"
    echo "  -d, --directory DIR   Specify the Roo Code MCP configuration directory"
    echo "                        Default: $DEFAULT_MCP_DIR"
    echo "  -h, --help            Display this help message and exit"
    echo ""
    echo "Example:"
    echo "  $0 --directory /custom/path/to/roo/mcp"
}

# Parse command line arguments
MCP_DIR="$DEFAULT_MCP_DIR"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -d|--directory)
            MCP_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Make sure all scripts are executable
chmod +x "$SCRIPT_DIR/roo-startup.sh"
chmod +x "$SCRIPT_DIR/register-mcp.sh"
chmod +x "$SCRIPT_DIR/manage-server.sh"

# Create the MCP configuration directory if it doesn't exist
mkdir -p "$MCP_DIR"

# Copy the MCP configuration file
echo "Copying MCP configuration to $MCP_DIR/simple-proxmox-mcp.json..."
cp "$SCRIPT_DIR/mcp.json" "$MCP_DIR/simple-proxmox-mcp.json"

# Update the working directory in the MCP configuration file
sed -i "s|\${__dirname}|$SCRIPT_DIR|g" "$MCP_DIR/simple-proxmox-mcp.json"

echo "Installation complete!"
echo ""
echo "The Simple Proxmox MCP server has been installed for Roo Code."
echo "Restart Roo Code to activate the MCP server."
echo ""
echo "For more information, see the ROO-INTEGRATION.md file."