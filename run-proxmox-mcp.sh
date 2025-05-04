#!/bin/bash

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Activate the virtual environment
cd "$SCRIPT_DIR/ProxmoxMCP"
source .venv-py312/bin/activate

# Set the configuration file path and environment variables
export PROXMOX_MCP_CONFIG="$SCRIPT_DIR/ProxmoxMCP/proxmox-config/config.json"
export PIP_USE_UV=1

# Run the ProxmoxMCP server
python -m proxmox_mcp.server