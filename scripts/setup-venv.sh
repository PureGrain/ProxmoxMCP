#!/bin/bash

# Script to set up the Python virtual environment with UV for ProxmoxMCP

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PATH="$SCRIPT_DIR/ProxmoxMCP/.venv-py312"
CONFIG_PATH="$SCRIPT_DIR/ProxmoxMCP/proxmox-config/config.json"

echo "Setting up Python virtual environment with UV for ProxmoxMCP..."

# Check if Python 3.10+ is installed
python_version=$(python3 --version 2>&1 | awk '{print $2}')
python_major=$(echo $python_version | cut -d. -f1)
python_minor=$(echo $python_version | cut -d. -f2)

if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 10 ]); then
    echo "Error: Python 3.10 or higher is required. Found Python $python_version"
    exit 1
fi

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "UV package manager not found. Installing UV..."
    pip install uv
fi

# Remove existing virtual environment if it exists
if [ -d "$VENV_PATH" ]; then
    echo "Removing existing virtual environment..."
    rm -rf "$VENV_PATH"
fi

# Create a new virtual environment using UV
echo "Creating new virtual environment with Python 3.12..."
uv venv "$VENV_PATH" --python=python3.12

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Install dependencies using UV
echo "Installing dependencies using UV..."
cd "$SCRIPT_DIR/ProxmoxMCP"
uv pip install -e .

# Install development dependencies if needed
if [ "$1" == "--dev" ]; then
    echo "Installing development dependencies..."
    uv pip install -e ".[dev]"
fi

# Set environment variable for UV
echo "Setting PIP_USE_UV=1 in the virtual environment..."
echo 'export PIP_USE_UV=1' >> "$VENV_PATH/bin/activate"

echo "Virtual environment setup complete!"
echo "To activate the virtual environment, run:"
echo "source $VENV_PATH/bin/activate"

# Make the script executable
chmod +x "$SCRIPT_DIR/setup-venv.sh"