"""
Main server implementation for Proxmox MCP.

This module implements the core MCP server for Proxmox integration, providing:
- Configuration loading and validation
- Logging setup
- Proxmox API connection management
- MCP tool registration and routing
- Signal handling for graceful shutdown

The server exposes a set of tools for managing Proxmox resources including:
- Node management
- VM operations
- Storage management
- Cluster status monitoring
"""
import logging
import os
import sys
import signal
from typing import Optional, List, Annotated, Dict, Any

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.tools import Tool
from mcp.types import TextContent as Content
from pydantic import Field

from .config.loader import load_config
from .core.logging import setup_logging
from .core.proxmox import ProxmoxManager
from .tools.node import NodeTools
from .tools.vm import VMTools
from .tools.vm_lifecycle import VMLifecycleTools
from .tools.storage import StorageTools
from .tools.cluster import ClusterTools
from .tools.task import TaskTools
from .tools.backup import BackupTools
from .tools.container import ContainerTools
from .tools.template import TemplateTools
from .tools.definitions import (
    GET_NODES_DESC,
    GET_NODE_STATUS_DESC,
    GET_VMS_DESC,
    EXECUTE_VM_COMMAND_DESC,
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
    GET_CONTAINER_TEMPLATES_DESC,
    GET_STORAGE_DESC,
    GET_CLUSTER_STATUS_DESC,
    START_VM_DESC,
    STOP_VM_DESC,
    REBOOT_VM_DESC,
    CREATE_VM_SNAPSHOT_DESC,
    LIST_VM_SNAPSHOTS_DESC,
    RESTORE_VM_SNAPSHOT_DESC,
    CLONE_VM_DESC,
    GET_VM_PERFORMANCE_DESC,
    GET_TASKS_DESC,
    GET_TASK_STATUS_DESC,
    CANCEL_TASK_DESC,
    CREATE_BACKUP_DESC,
    LIST_BACKUPS_DESC,
    RESTORE_BACKUP_DESC,
    GET_BACKUP_CONFIG_DESC,
    UPDATE_BACKUP_SCHEDULE_DESC,
    # Template tool descriptions
    GET_TEMPLATES_DESC,
    CREATE_TEMPLATE_DESC,
    CLONE_TEMPLATE_DESC,
    UPDATE_TEMPLATE_DESC,
    DELETE_TEMPLATE_DESC,
    IMPORT_TEMPLATE_DESC,
    GET_TEMPLATE_DETAILS_DESC
)

class ProxmoxMCPServer:
    """Main server class for Proxmox MCP."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the server.

        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
        self.logger = setup_logging(self.config.logging)

        # Initialize core components
        self.proxmox_manager = ProxmoxManager(self.config.proxmox, self.config.auth)
        self.proxmox = self.proxmox_manager.get_api()

        # Initialize tools
        self.node_tools = NodeTools(self.proxmox)
        self.vm_tools = VMTools(self.proxmox)
        self.vm_lifecycle_tools = VMLifecycleTools(self.proxmox)
        self.storage_tools = StorageTools(self.proxmox)
        self.cluster_tools = ClusterTools(self.proxmox)
        self.task_tools = TaskTools(self.proxmox)
        self.backup_tools = BackupTools(self.proxmox)
        self.container_tools = ContainerTools(self.proxmox)
        self.template_tools = TemplateTools(self.proxmox)

        # Initialize MCP server
        self.mcp = FastMCP("ProxmoxMCP")
        self._setup_tools()

    def _setup_tools(self) -> None:
        """Register MCP tools with the server.

        Initializes and registers all available tools with the MCP server:
        - Node management tools (list nodes, get status)
        - VM operation tools (list VMs, execute commands)
        - Storage management tools (list storage)
        - Cluster tools (get cluster status)

        Each tool is registered with appropriate descriptions and parameter
        validation using Pydantic models.
        """

        # Node tools
        @self.mcp.tool(description=GET_NODES_DESC)
        def get_nodes():
            return self.node_tools.get_nodes()

        @self.mcp.tool(description=GET_NODE_STATUS_DESC)
        def get_node_status(
            node: Annotated[str, Field(description="Name/ID of node to query (e.g. 'pve1', 'proxmox-node2')")]
        ):
            return self.node_tools.get_node_status(node)

        # VM tools
        @self.mcp.tool(description=GET_VMS_DESC)
        def get_vms():
            return self.vm_tools.get_vms()

        @self.mcp.tool(description=EXECUTE_VM_COMMAND_DESC)
        async def execute_vm_command(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number (e.g. '100', '101')")],
            command: Annotated[str, Field(description="Shell command to run (e.g. 'uname -a', 'systemctl status nginx')")]
        ):
            return await self.vm_tools.execute_command(node, vmid, command)

        # Storage tools
        @self.mcp.tool(description=GET_STORAGE_DESC)
        def get_storage():
            return self.storage_tools.get_storage()

        # VM lifecycle tools
        @self.mcp.tool(description=START_VM_DESC)
        def start_vm(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number (e.g. '100', '101')")]
        ):
            return self.vm_lifecycle_tools.start_vm(node, vmid)

        @self.mcp.tool(description=STOP_VM_DESC)
        def stop_vm(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number (e.g. '100', '101')")]
        ):
            return self.vm_lifecycle_tools.stop_vm(node, vmid)

        @self.mcp.tool(description=REBOOT_VM_DESC)
        def reboot_vm(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number (e.g. '100', '101')")]
        ):
            return self.vm_lifecycle_tools.reboot_vm(node, vmid)

        @self.mcp.tool(description=CREATE_VM_SNAPSHOT_DESC)
        def create_vm_snapshot(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number (e.g. '100', '101')")],
            name: Annotated[str, Field(description="Snapshot name (e.g. 'pre-update')")],
            description: Annotated[Optional[str], Field(description="Optional snapshot description")] = None
        ):
            return self.vm_lifecycle_tools.create_vm_snapshot(node, vmid, name, description)

        @self.mcp.tool(description=LIST_VM_SNAPSHOTS_DESC)
        def list_vm_snapshots(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number (e.g. '100', '101')")]
        ):
            return self.vm_lifecycle_tools.list_vm_snapshots(node, vmid)

        @self.mcp.tool(description=RESTORE_VM_SNAPSHOT_DESC)
        def restore_vm_snapshot(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number (e.g. '100', '101')")],
            snapshot_name: Annotated[str, Field(description="Name of the snapshot to restore")]
        ):
            return self.vm_lifecycle_tools.restore_vm_snapshot(node, vmid, snapshot_name)

        @self.mcp.tool(description=CLONE_VM_DESC)
        def clone_vm(
            node: Annotated[str, Field(description="Source host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Source VM ID number (e.g. '100', '101')")],
            target_vmid: Annotated[str, Field(description="Target VM ID number for the clone")],
            target_node: Annotated[Optional[str], Field(description="Optional target node (defaults to source node)")] = None,
            name: Annotated[Optional[str], Field(description="Optional name for the cloned VM")] = None
        ):
            return self.vm_lifecycle_tools.clone_vm(node, vmid, target_vmid, target_node, name)

        @self.mcp.tool(description=GET_VM_PERFORMANCE_DESC)
        def get_vm_performance(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number (e.g. '100', '101')")]
        ):
            return self.vm_lifecycle_tools.get_vm_performance(node, vmid)

        # Task management tools
        @self.mcp.tool(description=GET_TASKS_DESC)
        def get_tasks(
            limit: Annotated[int, Field(description="Maximum number of tasks to return")] = 50,
            vmid: Annotated[Optional[str], Field(description="Optional VM ID to filter tasks")] = None,
            node: Annotated[Optional[str], Field(description="Optional node name to filter tasks")] = None
        ):
            return self.task_tools.get_tasks(limit, vmid, node)

        @self.mcp.tool(description=GET_TASK_STATUS_DESC)
        def get_task_status(
            upid: Annotated[str, Field(description="Task UPID (Unique Process ID) to query")]
        ):
            return self.task_tools.get_task_status(upid)

        @self.mcp.tool(description=CANCEL_TASK_DESC)
        def cancel_task(
            upid: Annotated[str, Field(description="Task UPID (Unique Process ID) to cancel")]
        ):
            return self.task_tools.cancel_task(upid)

        # Backup management tools
        @self.mcp.tool(description=CREATE_BACKUP_DESC)
        def create_backup(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number (e.g. '100', '101')")],
            storage: Annotated[Optional[str], Field(description="Optional storage ID where to store the backup")] = None,
            compress: Annotated[Optional[str], Field(description="Optional compression algorithm (zstd, lzo, gzip)")] = None,
            mode: Annotated[str, Field(description="Backup mode (snapshot, suspend, stop)")] = "snapshot"
        ):
            return self.backup_tools.create_backup(node, vmid, storage, compress, mode)

        @self.mcp.tool(description=LIST_BACKUPS_DESC)
        def list_backups(
            storage: Annotated[Optional[str], Field(description="Optional storage ID to filter backups")] = None,
            vmid: Annotated[Optional[str], Field(description="Optional VM ID to filter backups")] = None
        ):
            return self.backup_tools.list_backups(storage, vmid)

        @self.mcp.tool(description=RESTORE_BACKUP_DESC)
        def restore_backup(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Original VM ID number")],
            backup_id: Annotated[str, Field(description="Backup volume ID to restore from")],
            target_storage: Annotated[Optional[str], Field(description="Optional storage ID for restored VM")] = None,
            target_vmid: Annotated[Optional[str], Field(description="Optional new VM ID for the restored VM")] = None
        ):
            return self.backup_tools.restore_backup(node, vmid, backup_id, target_storage, target_vmid)

        @self.mcp.tool(description=GET_BACKUP_CONFIG_DESC)
        def get_backup_config(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")]
        ):
            return self.backup_tools.get_backup_config(node)

        @self.mcp.tool(description=UPDATE_BACKUP_SCHEDULE_DESC)
        def update_backup_schedule(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            schedule: Annotated[Dict[str, Any], Field(description="Dictionary containing schedule configuration")]
        ):
            return self.backup_tools.update_backup_schedule(node, schedule)

        # Container tools
        @self.mcp.tool(description=GET_CONTAINERS_DESC)
        def get_containers():
            return self.container_tools.get_containers()

        @self.mcp.tool(description=GET_CONTAINER_STATUS_DESC)
        def get_container_status(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")]
        ):
            return self.container_tools.get_container_status(node, vmid)

        @self.mcp.tool(description=CREATE_CONTAINER_DESC)
        def create_container(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")],
            template: Annotated[str, Field(description="Template to use (e.g. 'local:vztmpl/ubuntu-20.04-standard_20.04-1_amd64.tar.gz')")],
            storage: Annotated[str, Field(description="Storage to use for container")],
            hostname: Annotated[Optional[str], Field(description="Optional hostname for the container")] = None,
            memory: Annotated[int, Field(description="Memory in MB")] = 512,
            cores: Annotated[int, Field(description="Number of CPU cores")] = 1,
            password: Annotated[Optional[str], Field(description="Optional root password")] = None,
            net0: Annotated[Optional[str], Field(description="Optional network configuration")] = None
        ):
            return self.container_tools.create_container(node, vmid, template, storage, hostname, memory, cores, password, net0)

        @self.mcp.tool(description=START_CONTAINER_DESC)
        def start_container(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")]
        ):
            return self.container_tools.start_container(node, vmid)

        @self.mcp.tool(description=STOP_CONTAINER_DESC)
        def stop_container(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")]
        ):
            return self.container_tools.stop_container(node, vmid)

        @self.mcp.tool(description=RESTART_CONTAINER_DESC)
        def restart_container(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")]
        ):
            return self.container_tools.restart_container(node, vmid)

        @self.mcp.tool(description=DELETE_CONTAINER_DESC)
        def delete_container(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")]
        ):
            return self.container_tools.delete_container(node, vmid)

        @self.mcp.tool(description=CLONE_CONTAINER_DESC)
        def clone_container(
            node: Annotated[str, Field(description="Source host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Source container ID number (e.g. '200', '201')")],
            target_vmid: Annotated[str, Field(description="Target container ID number for the clone")],
            target_node: Annotated[Optional[str], Field(description="Optional target node (defaults to source node)")] = None,
            name: Annotated[Optional[str], Field(description="Optional name for the cloned container")] = None
        ):
            return self.container_tools.clone_container(node, vmid, target_vmid, target_node, name)

        @self.mcp.tool(description=GET_CONTAINER_CONFIG_DESC)
        def get_container_config(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")]
        ):
            return self.container_tools.get_container_config(node, vmid)

        @self.mcp.tool(description=UPDATE_CONTAINER_CONFIG_DESC)
        def update_container_config(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")],
            **kwargs
        ):
            return self.container_tools.update_container_config(node, vmid, **kwargs)

        @self.mcp.tool(description=EXECUTE_CONTAINER_COMMAND_DESC)
        async def execute_container_command(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")],
            command: Annotated[str, Field(description="Shell command to run (e.g. 'uname -a')")]
        ):
            return await self.container_tools.execute_command(node, vmid, command)

        @self.mcp.tool(description=GET_CONTAINER_PERFORMANCE_DESC)
        def get_container_performance(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Container ID number (e.g. '200', '201')")]
        ):
            return self.container_tools.get_container_performance(node, vmid)

        @self.mcp.tool(description=GET_CONTAINER_TEMPLATES_DESC)
        def get_container_templates(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            storage: Annotated[Optional[str], Field(description="Optional storage ID to filter templates")] = None
        ):
            return self.container_tools.get_container_templates(node, storage)

        # Template tools
        @self.mcp.tool(description=GET_TEMPLATES_DESC)
        def get_templates():
            return self.template_tools.get_templates()

        @self.mcp.tool(description=CREATE_TEMPLATE_DESC)
        def create_template(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="VM ID number to convert to template (e.g. '100')")],
            name: Annotated[Optional[str], Field(description="Optional new name for the template")] = None,
            description: Annotated[Optional[str], Field(description="Optional description for the template")] = None
        ):
            return self.template_tools.create_template(node, vmid, name, description)

        @self.mcp.tool(description=CLONE_TEMPLATE_DESC)
        def clone_template(
            node: Annotated[str, Field(description="Source host node name (e.g. 'pve1', 'proxmox-node2')")],
            template_vmid: Annotated[str, Field(description="Template VM ID number (e.g. '100')")],
            name: Annotated[str, Field(description="Name for the new VM")],
            target_node: Annotated[Optional[str], Field(description="Optional target node (defaults to source node)")] = None,
            target_vmid: Annotated[Optional[str], Field(description="Optional specific VM ID for the clone")] = None,
            target_storage: Annotated[Optional[str], Field(description="Optional target storage for the clone")] = None,
            full_clone: Annotated[bool, Field(description="Whether to create a full clone (true) or linked clone (false)")] = True,
            description: Annotated[Optional[str], Field(description="Optional description for the new VM")] = None
        ):
            return self.template_tools.clone_template(node, template_vmid, name, target_node, target_vmid, target_storage, full_clone, description)

        @self.mcp.tool(description=UPDATE_TEMPLATE_DESC)
        def update_template(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Template VM ID number (e.g. '100')")],
            name: Annotated[Optional[str], Field(description="Optional new name for the template")] = None,
            description: Annotated[Optional[str], Field(description="Optional new description for the template")] = None,
            cores: Annotated[Optional[int], Field(description="Optional number of CPU cores")] = None,
            memory: Annotated[Optional[int], Field(description="Optional memory in MB")] = None
        ):
            return self.template_tools.update_template(node, vmid, name, description, cores, memory)

        @self.mcp.tool(description=DELETE_TEMPLATE_DESC)
        def delete_template(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Template VM ID number (e.g. '100')")]
        ):
            return self.template_tools.delete_template(node, vmid)

        @self.mcp.tool(description=IMPORT_TEMPLATE_DESC)
        def import_template(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            storage: Annotated[str, Field(description="Storage to use for the template")],
            url: Annotated[str, Field(description="URL to download the template from")],
            format: Annotated[Optional[str], Field(description="Optional format (e.g. 'qcow2', 'vmdk', 'raw')")] = None
        ):
            return self.template_tools.import_template(node, storage, url, format)

        @self.mcp.tool(description=GET_TEMPLATE_DETAILS_DESC)
        def get_template_details(
            node: Annotated[str, Field(description="Host node name (e.g. 'pve1', 'proxmox-node2')")],
            vmid: Annotated[str, Field(description="Template VM ID number (e.g. '100')")]
        ):
            return self.template_tools.get_template_details(node, vmid)

        # Cluster tools
        @self.mcp.tool(description=GET_CLUSTER_STATUS_DESC)
        def get_cluster_status():
            return self.cluster_tools.get_cluster_status()

    def start(self) -> None:
        """Start the MCP server.

        Initializes the server with:
        - Signal handlers for graceful shutdown (SIGINT, SIGTERM)
        - Async runtime for handling concurrent requests
        - Error handling and logging

        The server runs until terminated by a signal or fatal error.
        """
        import anyio

        def signal_handler(signum, frame):
            self.logger.info("Received signal to shutdown...")
            sys.exit(0)

        # Set up signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        try:
            self.logger.info("Starting MCP server...")
            anyio.run(self.mcp.run_stdio_async)
        except Exception as e:
            self.logger.error(f"Server error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    config_path = os.getenv("PROXMOX_MCP_CONFIG")
    if not config_path:
        print("PROXMOX_MCP_CONFIG environment variable must be set")
        sys.exit(1)

    try:
        server = ProxmoxMCPServer(config_path)
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
