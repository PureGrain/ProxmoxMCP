# Roo Code Integration for Simple Proxmox MCP

This directory contains scripts and configuration files to integrate the Simple Proxmox MCP server with Roo Code. The integration ensures that the MCP server starts automatically when Roo Code is launched, making Proxmox API tools available to Roo Code.

## Files

- `roo-startup.sh`: Script that starts the Proxmox MCP server when Roo Code is launched
- `register-mcp.sh`: Script that registers the MCP server with Roo Code
- `mcp.json`: Standard MCP configuration file for Roo Code integration
- `roo-mcp-config.json`: Alternative configuration file for custom integrations
- `manage-server.sh`: Original script to manage the MCP server (start, stop, status, etc.)

## Standard MCP Integration (Recommended)

The simplest way to integrate with Roo Code is using the standard MCP configuration:

1. Copy the `mcp.json` file to the Roo Code MCP configuration directory:
   ```bash
   cp mcp.json /path/to/roo/mcp/config/directory/
   ```

2. Make sure all scripts are executable:
   ```bash
   chmod +x roo-startup.sh manage-server.sh
   ```

3. Restart Roo Code, and the MCP server will automatically start and register itself.

## How It Works

The `mcp.json` file follows the standard MCP server configuration format:

- `name`: Identifies the MCP server to Roo Code
- `type`: Set to "stdio" for local execution
- `command`: The command to start the server
- `startup_command`: Executed when Roo Code starts
- `shutdown_command`: Executed when Roo Code shuts down
- `status_command`: Used to check if the server is running
- `working_directory`: Where the commands should be executed
- `auto_start`: Whether to start the server automatically
- `tools`: List of available tools with their descriptions and input schemas

When Roo Code starts:
1. It reads the `mcp.json` configuration
2. Executes the `startup_command` (`./roo-startup.sh`)
3. The startup script checks if the server is already running, and if not, starts it
4. Roo Code can now use the MCP server tools

## Manual Setup

To manually set up the integration:

1. Make sure all scripts are executable:
   ```bash
   chmod +x roo-startup.sh register-mcp.sh manage-server.sh
   ```

2. Test the startup script:
   ```bash
   ./roo-startup.sh
   ```

3. Test the registration script:
   ```bash
   ./register-mcp.sh
   ```

4. Verify the server is running:
   ```bash
   ./manage-server.sh status
   ```

## Available Tools

The following Proxmox API tools are available through this MCP server:

1. `get_nodes` - List all nodes in the Proxmox cluster
2. `get_node_status` - Get detailed status for a specific node
3. `get_vms` - List all VMs across the cluster
4. `execute_vm_command` - Execute commands in a VM via QEMU guest agent
5. `get_storage` - List storage pools across the cluster
6. `get_cluster_status` - Get overall Proxmox cluster health

## Troubleshooting

If the MCP server doesn't start automatically:

1. Check the log files:
   ```bash
   cat roo_startup.log
   cat mcp_registration.log
   cat simple_proxmox_mcp.log
   ```

2. Try starting the server manually:
   ```bash
   ./manage-server.sh start
   ```

3. Verify the configuration:
   ```bash
   cat mcp.json
   ```

4. Make sure the paths in the `mcp.json` file are correct for your system.

## Stopping the Server

When you're done using Roo Code, you can stop the MCP server:

```bash
./manage-server.sh stop
```

The server will also be stopped automatically when Roo Code shuts down, thanks to the `shutdown_command` in the `mcp.json` configuration.