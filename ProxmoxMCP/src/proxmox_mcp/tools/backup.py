"""
Backup management tools for Proxmox MCP.

This module provides tools for managing Proxmox backups:
- Creating VM and container backups
- Listing available backups
- Restoring from backups
- Managing backup schedules
- Configuring backup storage

These tools enable comprehensive backup management through the MCP interface,
providing essential functionality for systems administrators.
"""
from typing import Dict, List, Optional, Any
from mcp.types import TextContent as Content
from .base import ProxmoxTool

class BackupTools(ProxmoxTool):
    """Tools for managing Proxmox backups.
    
    Provides functionality for:
    - Creating VM and container backups
    - Listing available backups
    - Restoring from backups
    - Managing backup schedules
    - Configuring backup storage
    
    Essential for data protection and disaster recovery.
    """

    def create_backup(self, node: str, vmid: str, storage: Optional[str] = None, 
                     compress: Optional[str] = None, mode: str = "snapshot") -> List[Content]:
        """Create a backup of a VM or container.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number (e.g., '100', '101')
            storage: Optional storage ID where to store the backup
            compress: Optional compression algorithm (zstd, lzo, gzip)
            mode: Backup mode (snapshot, suspend, stop)

        Returns:
            List of Content objects containing operation result
        """
        try:
            params = {"vmid": vmid, "mode": mode}
            if storage:
                params["storage"] = storage
            if compress:
                params["compress"] = compress
                
            result = self.proxmox.nodes(node).vzdump.post(**params)
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Backup of VM {vmid} initiated"
            }, "backup_create")
        except Exception as e:
            self._handle_error(f"create backup for VM {vmid}", e)

    def list_backups(self, storage: Optional[str] = None, vmid: Optional[str] = None) -> List[Content]:
        """List available backups.

        Args:
            storage: Optional storage ID to filter backups
            vmid: Optional VM ID to filter backups

        Returns:
            List of Content objects containing backup information
        """
        try:
            backups = []
            
            # Get all nodes
            nodes = self.proxmox.nodes.get()
            
            # Collect backups from each node
            for node_info in nodes:
                node_name = node_info["node"]
                
                # Build filter parameters
                params = {}
                if storage:
                    params["storage"] = storage
                if vmid:
                    params["vmid"] = vmid
                    
                try:
                    # Get backups for this node
                    node_backups = self.proxmox.nodes(node_name).storage.get(**params)
                    
                    # Add each backup to our results
                    for backup in node_backups:
                        if backup.get("content") == "backup":
                            backups.append({
                                "filename": backup.get("volid", ""),
                                "node": node_name,
                                "vmid": backup.get("vmid", ""),
                                "size": backup.get("size", 0),
                                "timestamp": backup.get("ctime", 0),
                                "format": backup.get("format", "")
                            })
                except Exception:
                    # Skip if this node doesn't have backups
                    pass
                    
            return self._format_response(backups, "backups")
        except Exception as e:
            self._handle_error("list backups", e)

    def restore_backup(self, node: str, vmid: str, backup_id: str, 
                      target_storage: Optional[str] = None, target_vmid: Optional[str] = None) -> List[Content]:
        """Restore a VM or container from a backup.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Original VM ID number
            backup_id: Backup volume ID to restore from
            target_storage: Optional storage ID for restored VM
            target_vmid: Optional new VM ID for the restored VM

        Returns:
            List of Content objects containing operation result
        """
        try:
            params = {"vmid": vmid, "archive": backup_id}
            if target_storage:
                params["storage"] = target_storage
            if target_vmid:
                params["target_vmid"] = target_vmid
                
            result = self.proxmox.nodes(node).vzdump.extractconfig.post(**params)
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Restore of VM {vmid} from backup {backup_id} initiated"
            }, "backup_restore")
        except Exception as e:
            self._handle_error(f"restore VM {vmid} from backup", e)

    def get_backup_config(self, node: str) -> List[Content]:
        """Get backup schedule configuration for a node.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')

        Returns:
            List of Content objects containing backup configuration
        """
        try:
            config = self.proxmox.nodes(node).vzdump.extractconfig.get()
            return self._format_response(config, "backup_config")
        except Exception as e:
            self._handle_error(f"get backup configuration for node {node}", e)

    def update_backup_schedule(self, node: str, schedule: Dict[str, Any]) -> List[Content]:
        """Update backup schedule configuration for a node.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            schedule: Dictionary containing schedule configuration

        Returns:
            List of Content objects containing operation result
        """
        try:
            result = self.proxmox.nodes(node).vzdump.extractconfig.put(**schedule)
            return self._format_response({
                "success": True,
                "message": f"Backup schedule updated for node {node}"
            }, "backup_schedule_update")
        except Exception as e:
            self._handle_error(f"update backup schedule for node {node}", e)
