# Troubleshooting Guide

This guide provides solutions to common issues you might encounter when using ProxmoxMCP.

## Connection Issues

### Cannot Connect to Proxmox Server

**Symptoms**: The server fails to start or returns connection errors.

**Possible Solutions**:

1. **Check Network Connectivity**:
   ```bash
   ping your-proxmox-host
   ```

2. **Verify Proxmox API is Running**:
   ```bash
   curl -k https://your-proxmox-host:8006/api2/json/version
   ```

3. **Check Configuration**:
   - Verify the host, port, and authentication details in your config.json file
   - Ensure the API token has the necessary permissions

4. **SSL Certificate Issues**:
   - If using self-signed certificates, set `verify_ssl` to `false` in your configuration
   - If you need to use SSL verification, ensure your system trusts the certificate

### Authentication Failures

**Symptoms**: The server returns authentication errors.

**Possible Solutions**:

1. **Check API Token**:
   - Verify the token name and value in your configuration
   - Ensure the token has not expired
   - Create a new token if necessary

2. **Check User Permissions**:
   - Ensure the user has the necessary permissions in Proxmox
   - Check the Proxmox logs for permission-related errors

## Server Issues

### Server Won't Start

**Symptoms**: The server fails to start or crashes immediately.

**Possible Solutions**:

1. **Check Logs**:
   ```bash
   # Full Version
   cat proxmox_mcp.log
   
   # Simple Version
   cat simple_proxmox_mcp.log
   ```

2. **Check Port Availability**:
   - Ensure the port specified in your configuration is not in use
   - Try a different port if necessary

3. **Check Python Environment**:
   - Verify that all required packages are installed
   - Check for Python version compatibility issues

### Server Crashes

**Symptoms**: The server starts but crashes during operation.

**Possible Solutions**:

1. **Check Logs**:
   - Look for error messages in the log files
   - Increase the log level to DEBUG for more detailed information

2. **Memory Issues**:
   - Check if the server is running out of memory
   - Monitor resource usage during operation

3. **Update Dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## Tool Execution Issues

### Tool Returns Error

**Symptoms**: A specific tool returns an error when executed.

**Possible Solutions**:

1. **Check Parameters**:
   - Verify that all required parameters are provided
   - Check parameter types and formats

2. **Check Permissions**:
   - Ensure the API token has the necessary permissions for the operation
   - Check Proxmox logs for permission-related errors

3. **Check Resource Existence**:
   - Verify that the specified resources (nodes, VMs, etc.) exist
   - Check for typos in resource names or IDs

### Tool Hangs or Times Out

**Symptoms**: A tool execution takes too long or never completes.

**Possible Solutions**:

1. **Check Network Connectivity**:
   - Verify that the connection to the Proxmox server is stable
   - Check for network latency or packet loss

2. **Check Proxmox Load**:
   - Verify that the Proxmox server is not overloaded
   - Check Proxmox logs for performance issues

3. **Increase Timeout**:
   - If using the wait_for_task tool, increase the timeout parameter

## AI Assistant Integration Issues

### Augment Integration Issues

**Symptoms**: Augment cannot connect to the ProxmoxMCP server.

**Possible Solutions**:

1. **Check Server Status**:
   ```bash
   # Full Version
   ./ProxmoxMCP/manage-server.sh status
   
   # Simple Version
   ./simple-proxmox-mcp/manage-server.sh status
   ```

2. **Check Augment Configuration**:
   - Verify the path to the server script in your Augment settings
   - Ensure the server name is correct

3. **Restart VS Code**:
   - Close and reopen VS Code
   - Check if the Augment extension is loaded correctly

### RooCode/Cline Integration Issues

**Symptoms**: RooCode/Cline cannot connect to the ProxmoxMCP server.

**Possible Solutions**:

1. **Check Server Status**:
   ```bash
   # Full Version
   ./ProxmoxMCP/manage-server.sh status
   
   # Simple Version
   ./simple-proxmox-mcp/manage-server.sh status
   ```

2. **Check RooCode Configuration**:
   - Verify the path to the server script in your RooCode configuration
   - Ensure the server name is correct

3. **Check Logs**:
   ```bash
   cat simple-proxmox-mcp/roo_startup.log
   cat simple-proxmox-mcp/mcp_registration.log
   ```

4. **Manually Register the Server**:
   ```bash
   ./simple-proxmox-mcp/register-mcp.sh
   ```

## Common Error Messages

### "Connection refused"

**Possible Causes**:
- Proxmox server is not running
- Incorrect host or port in configuration
- Firewall blocking the connection

**Solutions**:
- Verify the Proxmox server is running
- Check the host and port in your configuration
- Check firewall settings

### "Authentication failed"

**Possible Causes**:
- Incorrect API token
- Token has expired
- User does not have the necessary permissions

**Solutions**:
- Verify the API token in your configuration
- Create a new token if necessary
- Check user permissions in Proxmox

### "SSL certificate verification failed"

**Possible Causes**:
- Self-signed certificate
- Certificate has expired
- Certificate is not trusted

**Solutions**:
- Set `verify_ssl` to `false` in your configuration
- Update the certificate
- Add the certificate to your trusted certificates

## Getting Help

If you continue to experience issues after trying the solutions in this guide:

1. Check the [GitHub Issues](https://github.com/yourusername/proxmox-mcp/issues) for similar problems
2. Create a new issue with detailed information about your problem
3. Include relevant logs and configuration details (remove sensitive information)
