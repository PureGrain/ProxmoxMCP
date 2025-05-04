# Script to set up the Python virtual environment with UV for ProxmoxMCP

# Get the absolute path to the script directory
$SCRIPT_DIR = $PSScriptRoot
$VENV_PATH = Join-Path $SCRIPT_DIR "ProxmoxMCP\.venv-py312"
$CONFIG_PATH = Join-Path $SCRIPT_DIR "ProxmoxMCP\proxmox-config\config.json"

Write-Host "Setting up Python virtual environment with UV for ProxmoxMCP..."

# Check if Python 3.10+ is installed
try {
    $pythonVersion = (python --version) -replace "Python ", ""
    $pythonMajor = [int]($pythonVersion -split '\.')[0]
    $pythonMinor = [int]($pythonVersion -split '\.')[1]

    if ($pythonMajor -lt 3 -or ($pythonMajor -eq 3 -and $pythonMinor -lt 10)) {
        Write-Host "Error: Python 3.10 or higher is required. Found Python $pythonVersion"
        exit 1
    }
} catch {
    Write-Host "Error: Python not found or unable to determine version."
    exit 1
}

# Check if UV is installed
try {
    $null = Get-Command uv -ErrorAction Stop
    Write-Host "UV package manager found."
} catch {
    Write-Host "UV package manager not found. Installing UV..."
    pip install uv
}

# Remove existing virtual environment if it exists
if (Test-Path $VENV_PATH) {
    Write-Host "Removing existing virtual environment..."
    Remove-Item -Recurse -Force $VENV_PATH
}

# Create a new virtual environment using UV
Write-Host "Creating new virtual environment with Python 3.12..."
uv venv $VENV_PATH --python=python3.12

# Activate the virtual environment
$activateScript = Join-Path $VENV_PATH "Scripts\Activate.ps1"
. $activateScript

# Install dependencies using UV
Write-Host "Installing dependencies using UV..."
Set-Location (Join-Path $SCRIPT_DIR "ProxmoxMCP")
uv pip install -e .

# Install development dependencies if needed
if ($args -contains "--dev") {
    Write-Host "Installing development dependencies..."
    uv pip install -e ".[dev]"
}

# Set environment variable for UV
Write-Host "Setting PIP_USE_UV=1 in the virtual environment..."
$activateContent = Get-Content $activateScript
$activateContent += "`n`$env:PIP_USE_UV = '1'"
Set-Content $activateScript $activateContent

Write-Host "Virtual environment setup complete!"
Write-Host "To activate the virtual environment, run:"
Write-Host ". $activateScript"