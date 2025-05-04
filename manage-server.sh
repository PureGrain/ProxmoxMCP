#!/bin/bash

# Script to manage the ProxmoxMCP server

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_PATH="$SCRIPT_DIR/ProxmoxMCP/proxmox-config/config.json"
VENV_PATH="$SCRIPT_DIR/ProxmoxMCP/.venv-py312"
LOG_FILE="$SCRIPT_DIR/ProxmoxMCP/proxmox_mcp.log"

# Function to start the server
start_server() {
    echo "Starting ProxmoxMCP server..."
    cd "$SCRIPT_DIR/ProxmoxMCP"
    source "$VENV_PATH/bin/activate"
    export PROXMOX_MCP_CONFIG="$CONFIG_PATH"
    export PIP_USE_UV=1
    nohup python -m proxmox_mcp.server > "$LOG_FILE" 2>&1 &
    echo "Server started with PID $!"
    echo "Log file: $LOG_FILE"
}

# Function to stop the server
stop_server() {
    echo "Stopping ProxmoxMCP server..."
    # Kill all processes related to proxmox_mcp.server
    pkill -f "proxmox_mcp.server"
    
    # Wait a moment to ensure all processes are terminated
    sleep 1
    
    # Check if any processes are still running
    if pgrep -f "proxmox_mcp.server" > /dev/null; then
        echo "Some processes are still running, forcing termination..."
        pkill -9 -f "proxmox_mcp.server"
    fi
    
    echo "All server processes stopped"
}

# Function to check server status
status_server() {
    if pgrep -f "python -m proxmox_mcp.server" > /dev/null; then
        echo "ProxmoxMCP server is running"
        ps aux | grep "python -m proxmox_mcp.server" | grep -v grep
    else
        echo "ProxmoxMCP server is not running"
    fi
}

# Function to view server logs
view_logs() {
    if [ -f "$LOG_FILE" ]; then
        echo "Showing last 20 lines of log file:"
        tail -n 20 "$LOG_FILE"
    else
        echo "Log file not found: $LOG_FILE"
    fi
}

# Function to test the server
test_server() {
    echo "Testing ProxmoxMCP server..."
    cd "$SCRIPT_DIR"
    source "$VENV_PATH/bin/activate"
    export PIP_USE_UV=1
    ./test-mcp.py
}

# Function to setup the virtual environment
setup_venv() {
    echo "Setting up virtual environment with UV..."
    cd "$SCRIPT_DIR"
    ./setup-venv.sh
}

# Main script logic
case "$1" in
    start)
        start_server
        ;;
    stop)
        stop_server
        ;;
    restart)
        stop_server
        sleep 2
        start_server
        ;;
    status)
        status_server
        ;;
    logs)
        view_logs
        ;;
    test)
        test_server
        ;;
    setup)
        setup_venv
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|test|setup}"
        exit 1
        ;;
esac

exit 0