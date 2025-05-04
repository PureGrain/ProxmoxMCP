#!/bin/bash

# Script to manage the Simple ProxmoxMCP server

# Get the absolute path to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_PATH="$SCRIPT_DIR/config.json"
LOG_FILE="$SCRIPT_DIR/simple_proxmox_mcp.log"

# Function to start the server
start_server() {
    echo "Starting Simple ProxmoxMCP server..."
    cd "$SCRIPT_DIR"
    # Use setsid to create a new session and disown the process
    setsid python3 server.py > "$LOG_FILE" 2>&1 &
    SERVER_PID=$!
    echo "Server started with PID $SERVER_PID"
    echo "Log file: $LOG_FILE"
    
    # Wait a moment to ensure the server is running
    sleep 2
    if ps -p $SERVER_PID > /dev/null; then
        echo "Server is running successfully"
    else
        echo "Server failed to start. Check the log file for errors."
    fi
}

# Function to stop the server
stop_server() {
    echo "Stopping Simple ProxmoxMCP server..."
    # Kill all processes related to the server
    pkill -f "python3 [^ ]*server\.py"
    
    # Wait a moment to ensure all processes are terminated
    sleep 1
    
    # Check if any processes are still running
    if pgrep -f "python3 [^ ]*server\.py" > /dev/null; then
        echo "Some processes are still running, forcing termination..."
        pkill -9 -f "python3 [^ ]*server\.py"
    fi
    
    echo "All server processes stopped"
}

# Function to check server status
status_server() {
    # Use a more specific pattern to find the server process
    if pgrep -f "python3 [^ ]*server\.py" > /dev/null; then
        echo "Simple ProxmoxMCP server is running"
        ps aux | grep "python3 .*server\.py" | grep -v grep
    else
        echo "Simple ProxmoxMCP server is not running"
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
    echo "Testing Simple ProxmoxMCP server..."
    cd "$SCRIPT_DIR"
    python3 server.py --info
    echo ""
    echo "Testing get_nodes tool..."
    python3 server.py --tool get_nodes
}

# Function to run a specific tool
run_tool() {
    if [ -z "$1" ]; then
        echo "Error: Tool name is required"
        echo "Usage: $0 run <tool_name> [arguments_json]"
        exit 1
    fi
    
    TOOL_NAME="$1"
    ARGUMENTS=""
    
    if [ ! -z "$2" ]; then
        ARGUMENTS="--arguments '$2'"
    fi
    
    echo "Running tool: $TOOL_NAME"
    cd "$SCRIPT_DIR"
    python3 server.py --tool "$TOOL_NAME" $ARGUMENTS
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
    run)
        shift
        run_tool "$@"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|test|run <tool_name> [arguments_json]}"
        exit 1
        ;;
esac

exit 0