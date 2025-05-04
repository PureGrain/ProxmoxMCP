# Using ProxmoxMCP with Cline

This guide explains how to use the ProxmoxMCP server with Cline.

## Setup

The ProxmoxMCP server has already been configured in your `.roo/mcp.json` file, so Cline should automatically detect and use it.

## Available Tools

The ProxmoxMCP server provides the following tools that you can use in Cline:

### get_nodes

Lists all nodes in the Proxmox cluster with their status, CPU, memory, and role information.

Example usage in Cline:
```
<use_mcp_tool>
<server_name>proxmox-mcp</server_name>
<tool_name>get_nodes</tool_name>
<arguments>
{}
</arguments>
</use_mcp_tool>
```

### get_node_status

Gets detailed status information for a specific Proxmox node.

Example usage in Cline:
```
<use_mcp_tool>
<server_name>proxmox-mcp</server_name>
<tool_name>get_node_status</tool_name>
<arguments>
{
  "node": "pve1"
}
</arguments>
</use_mcp_tool>
```

### get_vms

Lists all virtual machines across the cluster with their status and resource usage.

Example usage in Cline:
```
<use_mcp_tool>
<server_name>proxmox-mcp</server_name>
<tool_name>get_vms</tool_name>
<arguments>
{}
</arguments>
</use_mcp_tool>
```

### execute_vm_command

Executes commands in a VM via QEMU guest agent.

Example usage in Cline:
```
<use_mcp_tool>
<server_name>proxmox-mcp</server_name>
<tool_name>execute_vm_command</tool_name>
<arguments>
{
  "node": "pve1",
  "vmid": "100",
  "command": "uname -a"
}
</arguments>
</use_mcp_tool>
```

### get_storage

Lists storage pools across the cluster with their usage and configuration.

Example usage in Cline:
```
<use_mcp_tool>
<server_name>proxmox-mcp</server_name>
<tool_name>get_storage</tool_name>
<arguments>
{}
</arguments>
</use_mcp_tool>
```

### get_cluster_status

Gets overall Proxmox cluster health and configuration status.

Example usage in Cline:
```
<use_mcp_tool>
<server_name>proxmox-mcp</server_name>
<tool_name>get_cluster_status</tool_name>
<arguments>
{}
</arguments>
</use_mcp_tool>
```

## Troubleshooting

If you encounter any issues with the ProxmoxMCP server:

1. Check that the server is running: `ps aux | grep proxmox_mcp`
2. Check the log file: `cat ~/vscode/new-proxmox-mcp/ProxmoxMCP/proxmox_mcp.log`
3. Restart the server: `cd ~/vscode/new-proxmox-mcp && ./run-proxmox-mcp.sh`