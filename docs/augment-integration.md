# Augment Integration Guide

This guide provides instructions for integrating ProxmoxMCP with Augment, allowing you to manage your Proxmox infrastructure directly from the Augment AI assistant.

## Prerequisites

Before integrating ProxmoxMCP with Augment, ensure you have:

- ProxmoxMCP installed and configured
- VS Code with the Augment extension installed
- Access to a Proxmox VE server with API token credentials

## Integration Steps

### Option 1: Using the Augment Settings Panel

1. Open VS Code with the Augment extension installed
2. Click on the gear icon in the upper right corner of the Augment panel to open the Settings Panel
3. In the MCP servers section, add a new server with the following details:
   - **Name**: `proxmox-mcp` (or any name you prefer)
   - **Command**: The full path to the server script, e.g., `/path/to/proxmox-mcp/simple-proxmox-mcp/manage-server.sh`
   - **Args**: `start`

### Option 2: Editing settings.json Directly

Add the following configuration to your VS Code settings.json:

```json
"augment.advanced": {
    "mcpServers": [
        {
            "name": "proxmox-mcp",
            "command": "/path/to/proxmox-mcp/simple-proxmox-mcp/manage-server.sh",
            "args": ["start"]
        }
    ]
}
```

Replace `/path/to/proxmox-mcp` with the actual path to your ProxmoxMCP installation.

## Verifying Integration

To verify that ProxmoxMCP is integrated with Augment:

1. Open VS Code with the Augment extension
2. Open the Augment chat panel
3. Ask Augment to interact with your Proxmox server, for example:
   - "List all nodes in my Proxmox cluster"
   - "Show me all VMs on my Proxmox server"
   - "Get the status of node pve-host01"

Augment should be able to execute these commands and return the results.

## Example Prompts for Augment

Here are some example prompts you can use with Augment to interact with your Proxmox server:

### Basic Operations

- "List all nodes in my Proxmox cluster"
- "Show me the status of node pve-host01"
- "List all VMs across my Proxmox cluster"
- "Show me all storage pools in my Proxmox cluster"
- "Get the cluster status of my Proxmox server"

### VM Operations

- "Start VM 100 on node pve-host01"
- "Stop VM 100 on node pve-host01"
- "Reboot VM 100 on node pve-host01"
- "Create a snapshot of VM 100 on node pve-host01 called 'pre-update'"
- "List all snapshots for VM 100 on node pve-host01"
- "Restore VM 100 on node pve-host01 from snapshot 'pre-update'"
- "Clone VM 100 on node pve-host01 to create a new VM 101"

### Container Operations

- "List all containers in my Proxmox cluster"
- "Show me the status of container 200 on node pve-host01"
- "Start container 200 on node pve-host01"
- "Stop container 200 on node pve-host01"
- "Restart container 200 on node pve-host01"

### Task Management

- "List recent tasks in my Proxmox cluster"
- "Show me the status of task UPID:pve1:00051234:1234ABC:61A1B2C3:qmstart:100:root@pam:"

## Troubleshooting

If you encounter issues with the Augment integration:

1. Check that the ProxmoxMCP server is running:
   ```bash
   ./simple-proxmox-mcp/manage-server.sh status
   ```

2. Check the ProxmoxMCP log file for errors:
   ```bash
   cat simple-proxmox-mcp/simple_proxmox_mcp.log
   ```

3. Verify that the path to the ProxmoxMCP server script in your Augment settings is correct

4. Restart VS Code and try again

5. If issues persist, check the Augment extension logs for errors
