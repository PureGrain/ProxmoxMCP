   9i# Get the absolute path to the script directory
$SCRIPT_DIR = $PSScriptRoot

# Change to the ProxmoxMCP directory
Set-Location -Path "$SCRIPT_DIR\ProxmoxMCP"

# Activate the virtual environment
& .\.venv-py312\Scripts\Activate.ps1

# Set the configuration file path and environment variables
$env:PROXMOX_MCP_CONFIG = "$SCRIPT_DIR\ProxmoxMCP\proxmox-config\config.json"
$env:PIP_USE_UV = "1"

# Run the ProxmoxMCP server
python -m proxmox_mcp.server