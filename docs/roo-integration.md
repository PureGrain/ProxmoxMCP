# RooCode/Cline Integration Guide

This guide provides instructions for integrating ProxmoxMCP with RooCode/Cline, allowing you to manage your Proxmox infrastructure directly from the RooCode/Cline AI assistant.

## Prerequisites

Before integrating ProxmoxMCP with RooCode/Cline, ensure you have:

- ProxmoxMCP installed and configured
- RooCode/Cline installed
- Access to a Proxmox VE server with API token credentials

## Integration Steps

### Standard Integration

1. Create or edit the `.roo/mcp.json` file in your home directory:

```bash
mkdir -p ~/.roo
```

2. Add the following configuration to the `mcp.json` file:

```json
{
  "servers": [
    {
      "name": "proxmox-mcp",
      "type": "stdio",
      "command": "/path/to/proxmox-mcp/simple-proxmox-mcp/manage-server.sh start"
    }
  ]
}
```

Replace `/path/to/proxmox-mcp` with the actual path to your ProxmoxMCP installation.

### Using the Provided Scripts

The simple-proxmox-mcp directory includes scripts specifically for RooCode integration:

1. Make the scripts executable:

```bash
chmod +x /path/to/proxmox-mcp/simple-proxmox-mcp/roo-startup.sh
chmod +x /path/to/proxmox-mcp/simple-proxmox-mcp/register-mcp.sh
```

2. Run the registration script:

```bash
/path/to/proxmox-mcp/simple-proxmox-mcp/register-mcp.sh
```

This script will:
- Create the necessary directories
- Copy the MCP configuration file to the RooCode configuration directory
- Register the ProxmoxMCP server with RooCode

## Verifying Integration

To verify that ProxmoxMCP is integrated with RooCode/Cline:

1. Start RooCode/Cline
2. Ask RooCode/Cline to interact with your Proxmox server, for example:
   - "List all nodes in my Proxmox cluster"
   - "Show me all VMs on my Proxmox server"
   - "Get the status of node pve-host01"

RooCode/Cline should be able to execute these commands and return the results.

## Example Prompts for RooCode/Cline

Here are some example prompts you can use with RooCode/Cline to interact with your Proxmox server:

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

## Troubleshooting

If you encounter issues with the RooCode/Cline integration:

1. Check the log files:
   ```bash
   cat /path/to/proxmox-mcp/simple-proxmox-mcp/roo_startup.log
   cat /path/to/proxmox-mcp/simple-proxmox-mcp/mcp_registration.log
   cat /path/to/proxmox-mcp/simple-proxmox-mcp/simple_proxmox_mcp.log
   ```

2. Try starting the server manually:
   ```bash
   /path/to/proxmox-mcp/simple-proxmox-mcp/manage-server.sh start
   ```

3. Verify the configuration:
   ```bash
   cat ~/.roo/mcp.json
   ```

4. Make sure the paths in the `mcp.json` file are correct for your system.

5. Restart RooCode/Cline and try again.
