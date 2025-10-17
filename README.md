# ProxmoxMCP

> ⚠️ **This repository is deprecated. Please use the new, actively maintained repo:**  
> [ProxmoxEmCP](https://github.com/PureGrain/ProxmoxEmCP)

> This project is a fork of [canvrno/ProxmoxMCP](https://github.com/canvrno/ProxmoxMCP) with additional features and improvements.

A comprehensive Model Context Protocol (MCP) server for interacting with Proxmox hypervisors. This server provides a rich set of tools for managing Proxmox VE clusters, nodes, virtual machines, containers, backups, and tasks.

![ProxmoxMCP](https://github.com/user-attachments/assets/e32ab79f-be8a-420c-ab2d-475612150534)

## 🏗️ Built With

- [Proxmoxer](https://github.com/proxmoxer/proxmoxer) - Python wrapper for Proxmox API
- [MCP SDK](https://github.com/modelcontextprotocol/sdk) - Model Context Protocol SDK
- [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type annotations

## ✨ Features

- 🤖 Full integration with AI assistants (Augment, RooCode/Cline)
- 🛠️ Built with the official MCP SDK
- 🔒 Secure token-based authentication with Proxmox
- 🖥️ Comprehensive tools for managing nodes, VMs, and containers
- 💻 VM console command execution
- 📊 Task monitoring and management
- 📷 VM snapshot management
- 🔄 VM lifecycle operations (start, stop, reboot)
- 📦 Backup creation and restoration
- 📝 Configurable logging system
- ✅ Type-safe implementation with Pydantic
- 🎨 Rich output formatting with customizable themes

## Repository Structure

This repository contains two versions of ProxmoxMCP:

1. **Full Version** (`ProxmoxMCP/`): A comprehensive implementation with all features, built as a proper Python package.
2. **Simple Version** (`simple-proxmox-mcp/`): A lightweight, single-file implementation that's easier to set up and use.

Choose the version that best fits your needs:
- Use the **Full Version** for production environments or when you need all features
- Use the **Simple Version** for quick testing or simpler deployments

## Installation

### Prerequisites

- Python 3.10 or higher
- `proxmoxer` and `requests` Python packages
- Access to a Proxmox server with API token credentials

### Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/PureGrain/ProxmoxMCP.git
   cd proxmox-mcp
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the virtual environment (optional):
   ```bash
   # Linux/macOS
   ./scripts/setup-venv.sh
   
   # Windows
   .\scripts\setup-venv.ps1
   ```

4. Configure your Proxmox connection:
   ```bash
   # For full version
   cp ProxmoxMCP/proxmox-config/config.template.json ProxmoxMCP/proxmox-config/config.json
   
   # For simple version
   cp simple-proxmox-mcp/config.template.json simple-proxmox-mcp/config.json
   ```
   
   Edit the config.json file with your Proxmox credentials.

5. Start the server:
   ```bash
   # For full version
   ./ProxmoxMCP/run-proxmox-mcp.sh
   
   # For simple version
   ./simple-proxmox-mcp/manage-server.sh start
   ```

For detailed installation and usage instructions, see the [Full Documentation](docs/README.md).

## Integration with AI Assistants

ProxmoxMCP integrates with AI assistants like Augment and RooCode/Cline. See the integration guides:

- [Augment Integration](docs/augment-integration.md)
- [RooCode/Cline Integration](docs/roo-integration.md)

## Available Tools

ProxmoxMCP provides a wide range of tools for managing Proxmox resources:

- Node and cluster management
- VM lifecycle operations
- Container management
- Template operations
- Backup management
- Task monitoring
- And more...

For a complete list of available tools, see the [Tools Documentation](docs/tools.md).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The Proxmox team for their excellent API
- The MCP SDK team for the Model Context Protocol
- All contributors to this project
