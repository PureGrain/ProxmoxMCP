# PowerShell script to manage the ProxmoxMCP server

# Get the absolute path to the script directory
$SCRIPT_DIR = $PSScriptRoot
$CONFIG_PATH = "$SCRIPT_DIR\ProxmoxMCP\proxmox-config\config.json"
$VENV_PATH = "$SCRIPT_DIR\ProxmoxMCP\.venv-py312"
$LOG_FILE = "$SCRIPT_DIR\ProxmoxMCP\proxmox_mcp.log"

# Function to start the server
function Start-ProxmoxMCP {
    Write-Host "Starting ProxmoxMCP server..."
    Set-Location "$SCRIPT_DIR\ProxmoxMCP"
    & "$VENV_PATH\Scripts\Activate.ps1"
    $env:PROXMOX_MCP_CONFIG = $CONFIG_PATH
    $env:PIP_USE_UV = "1"
    Start-Process -FilePath "python" -ArgumentList "-m", "proxmox_mcp.server" -NoNewWindow
    Write-Host "Server started"
    Write-Host "Log file: $LOG_FILE"
}

# Function to stop the server
function Stop-ProxmoxMCP {
    Write-Host "Stopping ProxmoxMCP server..."
    
    # Kill all processes related to proxmox_mcp.server
    Get-Process | Where-Object { $_.CommandLine -like "*proxmox_mcp.server*" } | Stop-Process -Force
    
    # Wait a moment to ensure all processes are terminated
    Start-Sleep -Seconds 1
    
    # Check if any processes are still running
    $remainingProcesses = Get-Process | Where-Object { $_.CommandLine -like "*proxmox_mcp.server*" }
    if ($remainingProcesses) {
        Write-Host "Some processes are still running, forcing termination..."
        $remainingProcesses | Stop-Process -Force
    }
    
    Write-Host "All server processes stopped"
}

# Function to check server status
function Get-ProxmoxMCPStatus {
    $processes = Get-Process | Where-Object { $_.CommandLine -like "*python*proxmox_mcp.server*" }
    if ($processes) {
        Write-Host "ProxmoxMCP server is running"
        $processes | Format-Table Id, ProcessName, CPU, WorkingSet
    } else {
        Write-Host "ProxmoxMCP server is not running"
    }
}

# Function to view server logs
function Get-ProxmoxMCPLogs {
    if (Test-Path $LOG_FILE) {
        Write-Host "Showing last 20 lines of log file:"
        Get-Content $LOG_FILE -Tail 20
    } else {
        Write-Host "Log file not found: $LOG_FILE"
    }
}

# Function to test the server
function Test-ProxmoxMCP {
    Write-Host "Testing ProxmoxMCP server..."
    Set-Location $SCRIPT_DIR
    & "$VENV_PATH\Scripts\Activate.ps1"
    $env:PIP_USE_UV = "1"
    & ".\test-mcp.py"
}

# Function to setup the virtual environment
function Setup-VirtualEnvironment {
    Write-Host "Setting up virtual environment with UV..."
    Set-Location $SCRIPT_DIR
    & ".\setup-venv.ps1"
}

# Main script logic
switch ($args[0]) {
    "start" {
        Start-ProxmoxMCP
    }
    "stop" {
        Stop-ProxmoxMCP
    }
    "restart" {
        Stop-ProxmoxMCP
        Start-Sleep -Seconds 2
        Start-ProxmoxMCP
    }
    "status" {
        Get-ProxmoxMCPStatus
    }
    "logs" {
        Get-ProxmoxMCPLogs
    }
    "test" {
        Test-ProxmoxMCP
    }
    "setup" {
        Setup-VirtualEnvironment
    }
    default {
        Write-Host "Usage: .\manage-server.ps1 {start|stop|restart|status|logs|test|setup}"
    }
}