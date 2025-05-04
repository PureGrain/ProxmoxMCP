#!/bin/bash

# Script to start the Simple ProxmoxMCP server when Roo Code is launched
# This script should be executed when Roo Code starts

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MCP_SERVER_SCRIPT="$SCRIPT_DIR/manage-server.sh"
LOG_FILE="$SCRIPT_DIR/roo_startup.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Check if the server is already running
check_server_running() {
    if pgrep -f "python3 [^ ]*server\.py" > /dev/null; then
        return 0  # Server is running
    else
        return 1  # Server is not running
    fi
}

# Main execution
log_message "Roo Code startup detected - checking Proxmox MCP server status"

if check_server_running; then
    log_message "Proxmox MCP server is already running"
else
    log_message "Starting Proxmox MCP server..."
    "$MCP_SERVER_SCRIPT" start
    
    # Wait a moment to ensure the server is running
    sleep 2
    
    if check_server_running; then
        log_message "Proxmox MCP server started successfully"
        
        # Register the MCP server with Roo Code
        log_message "Server is now available for MCP requests"
        
        # Output MCP server information for Roo Code
        SERVER_INFO=$("$MCP_SERVER_SCRIPT" test | grep -A 20 "Testing Simple ProxmoxMCP server")
        log_message "Server information: $SERVER_INFO"
    else
        log_message "Failed to start Proxmox MCP server. Check logs for details."
    fi
fi

log_message "Roo Code startup script completed"
exit 0