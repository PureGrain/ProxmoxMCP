# AI Assistant Integration Guide

ProxmoxMCP can be integrated with AI assistants like Augment and RooCode/Cline, allowing you to manage your Proxmox infrastructure using natural language commands.

## Available Integrations

ProxmoxMCP currently supports the following AI assistant integrations:

- [Augment](augment-integration.md) - VS Code extension with AI capabilities
- [RooCode/Cline](roo-integration.md) - AI-powered command-line interface

## Benefits of AI Assistant Integration

Integrating ProxmoxMCP with an AI assistant provides several benefits:

1. **Natural Language Interface**: Manage your Proxmox infrastructure using natural language commands
2. **Contextual Understanding**: AI assistants understand the context of your requests
3. **Simplified Workflows**: Perform complex operations with simple commands
4. **Documentation Access**: Get help and documentation directly from the AI assistant
5. **Error Handling**: AI assistants can help troubleshoot issues

## How Integration Works

ProxmoxMCP implements the Model Context Protocol (MCP), which allows AI assistants to:

1. Discover available tools
2. Understand tool parameters and requirements
3. Execute tools with appropriate parameters
4. Process and display results

When you ask an AI assistant to perform a Proxmox-related task, it:

1. Analyzes your request to determine the appropriate tool
2. Extracts parameters from your request
3. Calls the ProxmoxMCP server to execute the tool
4. Presents the results in a user-friendly format

## Example Interactions

Here are some example interactions with AI assistants:

### Basic Operations

**User**: "List all nodes in my Proxmox cluster"
**AI**: *Executes the get_nodes tool and displays the results*

**User**: "Show me all VMs on my Proxmox server"
**AI**: *Executes the get_vms tool and displays the results*

### VM Management

**User**: "Start VM 100 on node pve-host01"
**AI**: *Executes the start_vm tool with the appropriate parameters*

**User**: "Create a snapshot of VM 100 called 'pre-update'"
**AI**: *Executes the create_vm_snapshot tool with the appropriate parameters*

### Complex Operations

**User**: "Clone VM template 110 to create a new VM called 'test-vm' with 2 CPUs and 4GB of RAM"
**AI**: *Executes multiple tools to clone the template and configure the new VM*

## Choosing an Integration

Choose the integration that best fits your workflow:

- **Augment**: If you primarily work in VS Code and prefer a graphical interface
- **RooCode/Cline**: If you prefer working in the terminal

You can also use both integrations simultaneously if needed.

## Getting Started

To get started with AI assistant integration, follow the specific integration guide for your preferred assistant:

- [Augment Integration Guide](augment-integration.md)
- [RooCode/Cline Integration Guide](roo-integration.md)
