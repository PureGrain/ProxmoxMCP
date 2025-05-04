# Configuration Guide

This guide provides detailed instructions for configuring ProxmoxMCP to connect to your Proxmox VE cluster.

## Configuration Files

ProxmoxMCP uses JSON configuration files to store connection details and settings:

- **Full Version**: `ProxmoxMCP/proxmox-config/config.json`
- **Simple Version**: `simple-proxmox-mcp/config.json`

## Basic Configuration

The basic configuration includes Proxmox connection details and authentication information:

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
    }
}
```

### Proxmox Connection Settings

- `host`: The hostname or IP address of your Proxmox VE server
- `port`: The port number for the Proxmox API (default: 8006)
- `verify_ssl`: Whether to verify SSL certificates (set to `false` for self-signed certificates)
- `service`: The Proxmox service to connect to (default: "PVE")

### Authentication Settings

ProxmoxMCP supports API token authentication:

- `user`: The Proxmox user in the format `username@realm` (e.g., `root@pam`)
- `token_name`: The name of the API token
- `token_value`: The value of the API token

## Advanced Configuration

### Logging Configuration

You can configure logging settings to control how ProxmoxMCP logs information:

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
        "file": "proxmox_mcp.log"
    }
}
```

### Logging Settings

- `level`: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `format`: The format of log messages
- `file`: The file to write logs to

## Creating an API Token in Proxmox

To create an API token in Proxmox VE:

1. Log in to the Proxmox web interface
2. Go to Datacenter > Permissions > API Tokens
3. Click "Add" to create a new token
4. Select a user and enter a token ID
5. Decide whether to grant privilege separation
6. Click "Create"
7. Save the token value (it will only be shown once)

## Testing Your Configuration

To test your configuration:

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

If the test is successful, you should see a list of nodes in your Proxmox cluster.

## Troubleshooting

If you encounter issues with your configuration:

1. Check that your Proxmox host is reachable from your machine
2. Verify that your API token has the necessary permissions
3. Check the log file for error messages
4. If using self-signed certificates, ensure `verify_ssl` is set to `false`
5. Verify that the port number is correct (default: 8006)

## Security Considerations

- Store your configuration files securely
- Use API tokens with the minimum necessary permissions
- Consider using environment variables for sensitive information
- Regularly rotate API tokens
- Use SSL/TLS for secure communication
