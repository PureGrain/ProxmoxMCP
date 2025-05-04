"""
VM lifecycle management tools for Proxmox MCP.

This module provides tools for managing the complete VM lifecycle:
- Creating new VMs from templates or ISO images
- Starting, stopping, and rebooting VMs
- Taking and restoring snapshots
- Cloning VMs
- Migrating VMs between nodes
- Monitoring VM performance metrics

These tools enable comprehensive VM management through the MCP interface,
providing essential functionality for systems administrators.
"""
from typing import Dict, List, Optional, Any
from mcp.types import TextContent as Content
from .base import ProxmoxTool

class VMLifecycleTools(ProxmoxTool):
    """Tools for managing VM lifecycle operations.
    
    Provides functionality for:
    - VM power operations (start, stop, reboot)
    - VM creation and provisioning
    - Snapshot management
    - VM cloning and migration
    - Performance monitoring
    
    Essential for day-to-day VM administration and management tasks.
    """

    def start_vm(self, node: str, vmid: str) -> List[Content]:
        """Start a virtual machine.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).qemu(vmid).status.start.post()
            return self._format_response({
                "success": True,
                "task_id": result.get("data"),
                "message": f"VM {vmid} start initiated"
            }, "vm_operation")
        except Exception as e:
            self._handle_error(f"start VM {vmid}", e)

    def stop_vm(self, node: str, vmid: str) -> List[Content]:
        """Stop a virtual machine.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).qemu(vmid).status.stop.post()
            return self._format_response({
                "success": True,
                "task_id": result.get("data"),
                "message": f"VM {vmid} stop initiated"
            }, "vm_operation")
        except Exception as e:
            self._handle_error(f"stop VM {vmid}", e)

    def reboot_vm(self, node: str, vmid: str) -> List[Content]:
        """Reboot a virtual machine.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).qemu(vmid).status.reboot.post()
            return self._format_response({
                "success": True,
                "task_id": result.get("data"),
                "message": f"VM {vmid} reboot initiated"
            }, "vm_operation")
        except Exception as e:
            self._handle_error(f"reboot VM {vmid}", e)

    def create_vm_snapshot(self, node: str, vmid: str, name: str, description: Optional[str] = None) -> List[Content]:
        """Create a snapshot of a virtual machine.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number (e.g., '100', '101')
            name: Snapshot name (e.g., 'pre-update', 'backup-20230601')
            description: Optional snapshot description

        Returns:
            List of Content objects containing operation result
        """
        try:
            params = {"snapname": name}
            if description:
                params["description"] = description
                
            result = self.proxmox.nodes(node).qemu(vmid).snapshot.post(**params)
            return self._format_response({
                "success": True,
                "task_id": result.get("data"),
                "message": f"Snapshot '{name}' creation initiated for VM {vmid}"
            }, "vm_snapshot")
        except Exception as e:
            self._handle_error(f"create snapshot for VM {vmid}", e)

    def list_vm_snapshots(self, node: str, vmid: str) -> List[Content]:
        """List all snapshots for a virtual machine.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing snapshot information
        """
        try:
            result = self.proxmox.nodes(node).qemu(vmid).snapshot.get()
            snapshots = []
            
            for snapshot in result:
                snapshots.append({
                    "name": snapshot.get("name"),
                    "description": snapshot.get("description", ""),
                    "creation_time": snapshot.get("snaptime", 0),
                    "parent": snapshot.get("parent", "")
                })
                
            return self._format_response(snapshots, "vm_snapshots")
        except Exception as e:
            self._handle_error(f"list snapshots for VM {vmid}", e)

    def restore_vm_snapshot(self, node: str, vmid: str, snapshot_name: str) -> List[Content]:
        """Restore a virtual machine from a snapshot.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number (e.g., '100', '101')
            snapshot_name: Name of the snapshot to restore

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).qemu(vmid).snapshot(snapshot_name).rollback.post()
            return self._format_response({
                "success": True,
                "task_id": result.get("data"),
                "message": f"VM {vmid} restore to snapshot '{snapshot_name}' initiated"
            }, "vm_snapshot_restore")
        except Exception as e:
            self._handle_error(f"restore VM {vmid} to snapshot '{snapshot_name}'", e)

    def clone_vm(self, node: str, vmid: str, target_vmid: str, target_node: Optional[str] = None, name: Optional[str] = None) -> List[Content]:
        """Clone a virtual machine.

        Args:
            node: Source host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Source VM ID number (e.g., '100', '101')
            target_vmid: Target VM ID number for the clone
            target_node: Optional target node (defaults to source node)
            name: Optional name for the cloned VM

        Returns:
            List of Content objects containing operation result
        """
        try:
            params = {"newid": target_vmid}
            if target_node:
                params["target"] = target_node
            if name:
                params["name"] = name
                
            result = self.proxmox.nodes(node).qemu(vmid).clone.post(**params)
            return self._format_response({
                "success": True,
                "task_id": result.get("data"),
                "message": f"VM {vmid} clone to {target_vmid} initiated"
            }, "vm_clone")
        except Exception as e:
            self._handle_error(f"clone VM {vmid} to {target_vmid}", e)

    def get_vm_performance(self, node: str, vmid: str) -> List[Content]:
        """Get performance metrics for a virtual machine.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing performance metrics
        """
        try:
            # Get current VM status for basic metrics
            status = self.proxmox.nodes(node).qemu(vmid).status.current.get()
            
            # Get RRD data for historical metrics if available
            try:
                rrd_data = self.proxmox.nodes(node).qemu(vmid).rrddata.get(timeframe="hour")
            except Exception:
                rrd_data = []
                
            # Compile performance metrics
            metrics = {
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
                "historical": rrd_data
            }
                
            return self._format_response(metrics, "vm_performance")
        except Exception as e:
            self._handle_error(f"get performance metrics for VM {vmid}", e)
