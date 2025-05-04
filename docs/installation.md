# Installation Guide

This guide provides detailed instructions for installing ProxmoxMCP on your system.

## Prerequisites

Before installing ProxmoxMCP, ensure you have the following:

- Python 3.10 or higher
- Access to a Proxmox VE server with API token credentials
- Git (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/proxmox-mcp.git
cd proxmox-mcp
```

### 2. Choose Your Version

ProxmoxMCP comes in two versions:

- **Full Version**: A comprehensive implementation with all features, built as a proper Python package.
- **Simple Version**: A lightweight, single-file implementation that's easier to set up and use.

Choose the version that best fits your needs.

### 3. Install Dependencies

#### Using pip

```bash
pip install -r requirements.txt
```

#### Using a Virtual Environment (Recommended)

##### Linux/macOS

```bash
# Make the script executable
chmod +x scripts/setup-venv.sh

# Run the setup script
./scripts/setup-venv.sh
```

##### Windows

```powershell
# Run the setup script
.\scripts\setup-venv.ps1
```

### 4. Configure ProxmoxMCP

#### Full Version

```bash
# Create a configuration file from the template
cp ProxmoxMCP/proxmox-config/config.template.json ProxmoxMCP/proxmox-config/config.json

# Edit the configuration file with your Proxmox credentials
nano ProxmoxMCP/proxmox-config/config.json
```

#### Simple Version

```bash
# Create a configuration file from the template
cp simple-proxmox-mcp/config.template.json simple-proxmox-mcp/config.json

# Edit the configuration file with your Proxmox credentials
nano simple-proxmox-mcp/config.json
```

### 5. Make Scripts Executable (Linux/macOS)

```bash
# Full Version
chmod +x ProxmoxMCP/run-proxmox-mcp.sh
chmod +x ProxmoxMCP/manage-server.sh

# Simple Version
chmod +x simple-proxmox-mcp/manage-server.sh
chmod +x simple-proxmox-mcp/setup.sh
```

## Running ProxmoxMCP

### Full Version

```bash
# Linux/macOS
./ProxmoxMCP/run-proxmox-mcp.sh

# Windows
.\ProxmoxMCP\run-proxmox-mcp.ps1
```

### Simple Version

```bash
# Linux/macOS
./simple-proxmox-mcp/manage-server.sh start

# Windows
.\simple-proxmox-mcp\manage-server.ps1 start
```

## Verifying Installation

To verify that ProxmoxMCP is installed and running correctly:

### Full Version

```bash
# Linux/macOS
./ProxmoxMCP/manage-server.sh status

# Windows
.\ProxmoxMCP\manage-server.ps1 status
```

### Simple Version

```bash
# Linux/macOS
./simple-proxmox-mcp/manage-server.sh status

# Windows
.\simple-proxmox-mcp\manage-server.ps1 status
```

You can also test the server by running a simple command:

### Full Version

```bash
# Linux/macOS
./ProxmoxMCP/manage-server.sh test

# Windows
.\ProxmoxMCP\manage-server.ps1 test
```

### Simple Version

```bash
# Linux/macOS
./simple-proxmox-mcp/manage-server.sh test

# Windows
.\simple-proxmox-mcp\manage-server.ps1 test
```

## Next Steps

Once you have ProxmoxMCP installed and running, you can:

1. [Configure ProxmoxMCP](configuration.md) for your specific needs
2. Explore the [Tools Documentation](tools.md) to learn about the available tools
3. Set up [AI Assistant Integration](integration.md) with Augment or RooCode/Cline
