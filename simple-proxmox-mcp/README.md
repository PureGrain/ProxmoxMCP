# Simple Proxmox MCP

A lightweight Model Context Protocol (MCP) server for interacting with Proxmox VE API. This MCP server provides comprehensive tools to query and manage Proxmox VE clusters, nodes, virtual machines, and templates.

## Features

- Lightweight implementation of the MCP protocol
- Direct interaction with Proxmox VE API
- Complete VM lifecycle management (create, configure, start, stop, reboot)
- Template-based VM deployment
- Resource management (CPU, memory, storage)
- Task monitoring and management
- Integration with AI assistants (Augment, RooCode/Cline)

## Requirements

- Python 3.6+
- `proxmoxer` and `requests` Python packages
- Proxmox VE API token

## Configuration

Edit the `config.json` file to configure the connection to your Proxmox VE cluster:

```json
{
    "proxmox": {
        "host": "your-proxmox-host",
        "port": 8006,
        "verify_ssl": false,
        "service": "PVE"
    },
    "auth": {
        "user": "root@pam",
        "token_name": "your-token-name",
        "token_value": "your-token-value"
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "simple_proxmox_mcp.log"
    }
}
```

## Usage

### Managing the Server

The `manage-server.sh` script provides commands to manage the MCP server:

```bash
# Start the server
./manage-server.sh start

# Stop the server
./manage-server.sh stop

# Restart the server
./manage-server.sh restart

# Check server status
./manage-server.sh status

# View server logs
./manage-server.sh logs

# Test the server
./manage-server.sh test

# Run a specific tool
./manage-server.sh run get_nodes
./manage-server.sh run get_node_status '{"node": "pve-host01"}'
```

## Available Tools

The MCP server provides the following tools:

### Basic Operations

- `get_nodes`: List all nodes in the Proxmox cluster with their status, CPU, memory, and role information
- `get_node_status`: Get detailed status information for a specific Proxmox node
- `get_vms`: List all virtual machines across the cluster with their status and resource usage
- `execute_vm_command`: Execute commands in a VM via QEMU guest agent
- `get_storage`: List storage pools across the cluster with their usage and configuration
- `get_cluster_status`: Get overall Proxmox cluster health and configuration status

### Template Operations

- `get_templates`: List all VM templates available across the cluster
- `clone_template`: Clone a VM template to create a new VM

### VM Power Operations

- `start_vm`: Start a VM
- `stop_vm`: Shutdown a VM gracefully
- `reboot_vm`: Reboot a VM gracefully

### VM Configuration Operations

- `update_vm_config`: Update VM configuration (CPU, memory, name, description)
- `get_vm_config`: Get detailed VM configuration

### Task Operations

- `get_task_status`: Get the status of a task
- `wait_for_task`: Wait for a task to complete

## Example Usage

### Command Examples

```bash
# List all nodes
./manage-server.sh run get_nodes

# Get detailed node status
./manage-server.sh run get_node_status '{"node": "pve-host01"}'

# List all VMs
./manage-server.sh run get_vms

# Execute a command in a VM
./manage-server.sh run execute_vm_command '{"node": "pve-host01", "vmid": "100", "command": "uname -a"}'

# List storage pools
./manage-server.sh run get_storage

# Get cluster status
./manage-server.sh run get_cluster_status
```

### VM Lifecycle Management

```bash
# List available templates
./manage-server.sh run get_templates

# Clone a template to create a new VM
./manage-server.sh run clone_template '{"node": "pve-host01", "template_vmid": "110", "new_vm_name": "test-vm-from-template", "full_clone": true}'

# Update VM configuration
./manage-server.sh run update_vm_config '{"node": "pve-host01", "vmid": "109", "cpu": 2, "memory": 4096, "description": "Test VM created from template"}'

# Start the VM
./manage-server.sh run start_vm '{"node": "pve-host01", "vmid": "109"}'

# Get VM configuration
./manage-server.sh run get_vm_config '{"node": "pve-host01", "vmid": "109"}'

# Stop the VM
./manage-server.sh run stop_vm '{"node": "pve-host01", "vmid": "109"}'

# Reboot the VM
./manage-server.sh run reboot_vm '{"node": "pve-host01", "vmid": "109"}'
```

### Task Management

```bash
# Get task status
./manage-server.sh run get_task_status '{"node": "pve-host01", "task_id": "UPID:pve-host01:00000000:00000000:00000000:qmclone:100:root@pam:"}'

# Wait for task to complete
./manage-server.sh run wait_for_task '{"node": "pve-host01", "task_id": "UPID:pve-host01:00000000:00000000:00000000:qmclone:100:root@pam:", "timeout": 120}'
```

## Integration with AI Assistants

### RooCode/Cline Integration

To connect to the ProxmoxMCP server from RooCode/Cline, add the following to your `.roo/mcp.json` file:

```json
{
  "servers": [
    {
      "name": "proxmox-mcp",
      "type": "stdio",
      "command": "/path/to/new-proxmox-mcp/simple-proxmox-mcp/manage-server.sh start"
    }
  ]
}
```

### Augment Integration

To connect to the ProxmoxMCP server from Augment:

#### Option 1: Using the Augment Settings Panel

1. Open VS Code with the Augment extension installed
2. Click on the gear icon in the upper right corner of the Augment panel to open the Settings Panel
3. In the MCP servers section, add a new server with the following details:
   - **Name**: `proxmox-mcp` (or any name you prefer)
   - **Command**: The full path to the server script, e.g., `/path/to/new-proxmox-mcp/simple-proxmox-mcp/manage-server.sh`
   - **Args**: `start`

#### Option 2: Editing settings.json Directly

Add the following configuration to your VS Code settings.json:

```json
"augment.advanced": {
    "mcpServers": [
        {
            "name": "proxmox-mcp",
            "command": "/path/to/new-proxmox-mcp/simple-proxmox-mcp/manage-server.sh",
            "args": ["start"]
        }
    ]
}
```

## Troubleshooting

If you encounter issues:

1. Check the log file (`simple_proxmox_mcp.log`) for error messages
2. Verify your Proxmox API token is valid and has the necessary permissions
3. Ensure the Proxmox host is reachable from your machine
4. Check that the required Python packages are installed
5. For template cloning issues, ensure the template is not locked or in use
6. For VM power operations, check that the VM is in the appropriate state

## License

MIT