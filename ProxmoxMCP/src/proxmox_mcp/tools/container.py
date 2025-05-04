"""
Container management tools for Proxmox MCP.

This module provides tools for managing and interacting with Proxmox LXC containers:
- Listing all containers across the cluster with their status
- Creating, starting, stopping, and deleting containers
- Retrieving detailed container information including:
  * Resource allocation (CPU, memory)
  * Runtime status
  * Node placement
- Executing commands within containers
- Managing container configuration

The tools implement fallback mechanisms for scenarios where
detailed container information might be temporarily unavailable.
"""
from typing import List, Dict, Any, Optional
from mcp.types import TextContent as Content
from .base import ProxmoxTool
from .definitions import (
    GET_CONTAINERS_DESC, 
    GET_CONTAINER_STATUS_DESC,
    CREATE_CONTAINER_DESC,
    START_CONTAINER_DESC,
    STOP_CONTAINER_DESC,
    RESTART_CONTAINER_DESC,
    DELETE_CONTAINER_DESC,
    CLONE_CONTAINER_DESC,
    GET_CONTAINER_CONFIG_DESC,
    UPDATE_CONTAINER_CONFIG_DESC,
    EXECUTE_CONTAINER_COMMAND_DESC,
    GET_CONTAINER_PERFORMANCE_DESC,
    GET_CONTAINER_TEMPLATES_DESC
)

class ContainerTools(ProxmoxTool):
    """Tools for managing Proxmox LXC containers.
    
    Provides functionality for:
    - Retrieving cluster-wide container information
    - Getting detailed container status and configuration
    - Creating, starting, stopping, and deleting containers
    - Cloning containers
    - Executing commands within containers
    - Managing container configuration
    
    Implements fallback mechanisms for scenarios where detailed
    container information might be temporarily unavailable.
    """

    def __init__(self, proxmox_api):
        """Initialize container tools.

        Args:
            proxmox_api: Initialized ProxmoxAPI instance
        """
        super().__init__(proxmox_api)

    def get_containers(self) -> List[Content]:
        """List all LXC containers across the cluster with their status and configuration.

        Returns:
            List of Content objects containing container information
        """
        try:
            # Get all nodes in the cluster
            nodes = self.proxmox.nodes.get()
            
            # Collect containers from all nodes
            containers = []
            for node in nodes:
                node_name = node['node']
                try:
                    node_containers = self.proxmox.nodes(node_name).lxc.get()
                    for container in node_containers:
                        container['node'] = node_name
                        containers.append(container)
                except Exception as e:
                    self.logger.warning(f"Failed to get containers for node {node_name}: {str(e)}")
            
            # Format and return the container list
            return self._format_response(containers, "container_list")
        except Exception as e:
            self._handle_error("get containers", e)

    def get_container_status(self, node: str, vmid: str) -> List[Content]:
        """Get detailed status information for a specific container.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing container status
        """
        try:
            # Get container status
            status = self.proxmox.nodes(node).lxc(vmid).status.current.get()
            
            # Get container config for additional information
            config = self.proxmox.nodes(node).lxc(vmid).config.get()
            
            # Combine status and config information
            result = {
                "vmid": vmid,
                "node": node,
                "status": status.get("status", "unknown"),
                "name": config.get("hostname", ""),
                "cpu": {
                    "cores": config.get("cores", 1),
                    "usage": status.get("cpu", 0)
                },
                "memory": {
                    "used": status.get("mem", 0),
                    "total": config.get("memory", 512) * 1024 * 1024
                },
                "uptime": status.get("uptime", 0),
                "disk": status.get("disk", {}),
                "network": status.get("netout", {})
            }
            
            return self._format_response(result, "container_status")
        except Exception as e:
            self._handle_error(f"get container {vmid} status", e)

    def create_container(self, node: str, vmid: str, template: str, storage: str, 
                        hostname: Optional[str] = None, memory: int = 512, 
                        cores: int = 1, password: Optional[str] = None, 
                        net0: Optional[str] = None) -> List[Content]:
        """Create a new container from a template.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')
            template: Template to use (e.g., 'local:vztmpl/ubuntu-20.04-standard_20.04-1_amd64.tar.gz')
            storage: Storage to use for container
            hostname: Optional hostname for the container
            memory: Memory in MB (default: 512)
            cores: Number of CPU cores (default: 1)
            password: Optional root password
            net0: Optional network configuration

        Returns:
            List of Content objects containing operation result
        """
        try:
            # Prepare container creation parameters
            params = {
                "vmid": vmid,
                "ostemplate": template,
                "storage": storage,
                "memory": memory,
                "cores": cores
            }
            
            # Add optional parameters if provided
            if hostname:
                params["hostname"] = hostname
            if password:
                params["password"] = password
            if net0:
                params["net0"] = net0
            
            # Create the container
            result = self.proxmox.nodes(node).lxc.post(**params)
            
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Container {vmid} creation initiated"
            }, "container_operation")
        except Exception as e:
            self._handle_error(f"create container {vmid}", e)

    def start_container(self, node: str, vmid: str) -> List[Content]:
        """Start a container.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).lxc(vmid).status.start.post()
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Container {vmid} start initiated"
            }, "container_operation")
        except Exception as e:
            self._handle_error(f"start container {vmid}", e)

    def stop_container(self, node: str, vmid: str) -> List[Content]:
        """Stop a container.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).lxc(vmid).status.stop.post()
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Container {vmid} stop initiated"
            }, "container_operation")
        except Exception as e:
            self._handle_error(f"stop container {vmid}", e)

    def restart_container(self, node: str, vmid: str) -> List[Content]:
        """Restart a container.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).lxc(vmid).status.restart.post()
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Container {vmid} restart initiated"
            }, "container_operation")
        except Exception as e:
            self._handle_error(f"restart container {vmid}", e)

    def delete_container(self, node: str, vmid: str) -> List[Content]:
        """Delete a container.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).lxc(vmid).delete.post()
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Container {vmid} deletion initiated"
            }, "container_operation")
        except Exception as e:
            self._handle_error(f"delete container {vmid}", e)

    def clone_container(self, node: str, vmid: str, target_vmid: str, 
                       target_node: Optional[str] = None, 
                       name: Optional[str] = None) -> List[Content]:
        """Clone a container.

        Args:
            node: Source host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Source container ID number (e.g., '100', '101')
            target_vmid: Target container ID number for the clone
            target_node: Optional target node (defaults to source node)
            name: Optional name for the cloned container

        Returns:
            List of Content objects containing operation result
        """
        try:
            params = {"newid": target_vmid}
            if target_node:
                params["target"] = target_node
            if name:
                params["hostname"] = name
                
            result = self.proxmox.nodes(node).lxc(vmid).clone.post(**params)
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Container {vmid} clone to {target_vmid} initiated"
            }, "container_clone")
        except Exception as e:
            self._handle_error(f"clone container {vmid} to {target_vmid}", e)

    def get_container_config(self, node: str, vmid: str) -> List[Content]:
        """Get detailed configuration for a container.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing container configuration
        """
        try:
            config = self.proxmox.nodes(node).lxc(vmid).config.get()
            return self._format_response(config, "container_config")
        except Exception as e:
            self._handle_error(f"get container {vmid} config", e)

    def update_container_config(self, node: str, vmid: str, **kwargs) -> List[Content]:
        """Update container configuration.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')
            **kwargs: Configuration parameters to update

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).lxc(vmid).config.put(**kwargs)
            return self._format_response({
                "success": True,
                "message": f"Container {vmid} configuration updated"
            }, "container_config_update")
        except Exception as e:
            self._handle_error(f"update container {vmid} config", e)

    async def execute_command(self, node: str, vmid: str, command: str) -> List[Content]:
        """Execute a command in a container.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')
            command: Shell command to run (e.g., 'uname -a')

        Returns:
            List of Content objects containing command execution result
        """
        try:
            # For LXC containers, we need to use the exec endpoint
            result = self.proxmox.nodes(node).lxc(vmid).exec.post(
                command=command
            )
            
            # Wait for the command to complete and get the output
            task_id = result
            task_status = self.proxmox.nodes(node).tasks(task_id).status.get()
            
            # Process the command output
            output = ""
            exit_code = 0
            
            if task_status.get("exitstatus") == "OK":
                # Get the command output from the task log
                task_log = self.proxmox.nodes(node).tasks(task_id).log.get()
                output = "\n".join([entry.get("t", "") for entry in task_log])
            else:
                exit_code = 1
                output = f"Command execution failed: {task_status.get('exitstatus', 'Unknown error')}"
            
            return self._format_response({
                "success": exit_code == 0,
                "output": output,
                "exit_code": exit_code
            }, "container_command")
        except Exception as e:
            self._handle_error(f"execute command in container {vmid}", e)

    def get_container_performance(self, node: str, vmid: str) -> List[Content]:
        """Get performance metrics for a container.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Container ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing performance metrics
        """
        try:
            # Get current status for real-time metrics
            status = self.proxmox.nodes(node).lxc(vmid).status.current.get()
            
            # Get RRD data for historical metrics if available
            try:
                rrd_data = self.proxmox.nodes(node).lxc(vmid).rrddata.get()
            except:
                rrd_data = []
            
            # Format the performance data
            performance = {
                "cpu_usage": status.get("cpu", 0),
                "memory": {
                    "used": status.get("mem", 0),
                    "total": status.get("maxmem", 0)
                },
                "disk_io": {
                    "read_bytes": status.get("diskread", 0),
                    "write_bytes": status.get("diskwrite", 0)
                },
                "network": {
                    "in_bytes": status.get("netin", 0),
                    "out_bytes": status.get("netout", 0)
                },
                "historical_data": rrd_data
            }
            
            return self._format_response(performance, "container_performance")
        except Exception as e:
            self._handle_error(f"get container {vmid} performance", e)

    def get_container_templates(self, node: str, storage: Optional[str] = None) -> List[Content]:
        """Get available container templates.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            storage: Optional storage ID to filter templates

        Returns:
            List of Content objects containing template information
        """
        try:
            params = {}
            if storage:
                params["storage"] = storage
                
            templates = self.proxmox.nodes(node).storage.get(**params)
            
            # Filter for container templates
            container_templates = []
            for template in templates:
                if template.get("content", "").startswith("vztmpl"):
                    container_templates.append(template)
            
            return self._format_response(container_templates, "container_templates")
        except Exception as e:
            self._handle_error("get container templates", e)
