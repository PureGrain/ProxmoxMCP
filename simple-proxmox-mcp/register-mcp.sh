#!/bin/bash

# Script to register the Simple ProxmoxMCP server with Roo Code
# This script should be executed during Roo Code initialization

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MCP_SERVER_SCRIPT="$SCRIPT_DIR/manage-server.sh"
ROO_STARTUP_SCRIPT="$SCRIPT_DIR/roo-startup.sh"
LOG_FILE="$SCRIPT_DIR/mcp_registration.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to get server information
get_server_info() {
    "$MCP_SERVER_SCRIPT" test | grep -A 20 "Testing Simple ProxmoxMCP server"
}

# Main execution
log_message "Registering Proxmox MCP server with Roo Code"

# First, ensure the server is running by executing the startup script
log_message "Ensuring server is running..."
"$ROO_STARTUP_SCRIPT"

# Get server information for registration
SERVER_INFO=$(get_server_info)
log_message "Server information: $SERVER_INFO"

# Output MCP server registration information in the format expected by Roo Code
cat << EOF
{
  "mcp_server": {
    "name": "simple-proxmox-mcp",
    "version": "1.0.0",
    "description": "Simple MCP server for Proxmox API",
    "status": "ready",
    "tools": [
      "get_nodes",
      "get_node_status",
      "get_vms",
      "execute_vm_command",
      "get_storage",
      "get_cluster_status"
    ]
  }
}
EOF

log_message "MCP server registration completed"
exit 0