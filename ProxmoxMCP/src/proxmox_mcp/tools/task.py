"""
Task management tools for Proxmox MCP.

This module provides tools for managing and monitoring Proxmox tasks:
- Listing active and recent tasks across the cluster
- Getting detailed task information and status
- Monitoring task progress
- Cancelling running tasks

These tools enable comprehensive task management through the MCP interface,
providing essential functionality for systems administrators.
"""
from typing import Dict, List, Optional, Any
from mcp.types import TextContent as Content
from .base import ProxmoxTool

class TaskTools(ProxmoxTool):
    """Tools for managing Proxmox tasks.
    
    Provides functionality for:
    - Listing active and recent tasks
    - Getting detailed task information
    - Monitoring task progress
    - Cancelling running tasks
    
    Essential for tracking operations and troubleshooting issues.
    """

    def get_tasks(self, limit: int = 50, vmid: Optional[str] = None, node: Optional[str] = None) -> List[Content]:
        """List recent tasks across the cluster with their status.

        Args:
            limit: Maximum number of tasks to return (default: 50)
            vmid: Optional VM ID to filter tasks for a specific VM
            node: Optional node name to filter tasks for a specific node

        Returns:
            List of Content objects containing formatted task information
        """
        try:
            tasks = []
            
            # If node is specified, get tasks for that node only
            if node:
                nodes = [{"node": node}]
            else:
                # Otherwise get all nodes
                nodes = self.proxmox.nodes.get()
                
            # Collect tasks from each node
            for node_info in nodes:
                node_name = node_info["node"]
                
                # Build filter parameters
                params = {"limit": limit}
                if vmid:
                    params["vmid"] = vmid
                    
                # Get tasks for this node
                node_tasks = self.proxmox.nodes(node_name).tasks.get(**params)
                
                # Add each task to our results
                for task in node_tasks:
                    tasks.append({
                        "upid": task.get("upid", ""),
                        "type": task.get("type", ""),
                        "status": task.get("status", ""),
                        "node": node_name,
                        "starttime": task.get("starttime", 0),
                        "endtime": task.get("endtime", 0),
                        "id": task.get("id", ""),
                        "user": task.get("user", ""),
                        "vmid": task.get("vmid", "")
                    })
                    
                    # If we've reached the limit, stop collecting tasks
                    if len(tasks) >= limit:
                        break
                        
                # If we've reached the limit, stop collecting tasks
                if len(tasks) >= limit:
                    break
                    
            return self._format_response(tasks, "tasks")
        except Exception as e:
            self._handle_error("get tasks", e)

    def get_task_status(self, upid: str) -> List[Content]:
        """Get detailed status for a specific task.

        Args:
            upid: Task UPID (Unique Process ID) to query

        Returns:
            List of Content objects containing detailed task status
        """
        try:
            # Parse node from UPID
            node = upid.split(':')[1]
            
            # Get task status
            status = self.proxmox.nodes(node).tasks(upid).status.get()
            
            # Format the response
            result = {
                "upid": upid,
                "node": node,
                "type": status.get("type", ""),
                "status": status.get("status", ""),
                "exitstatus": status.get("exitstatus", ""),
                "user": status.get("user", ""),
                "starttime": status.get("starttime", 0),
                "pid": status.get("pid", 0),
                "progress": status.get("progress", 0),
                "log": self._get_task_log(node, upid)
            }
                
            return self._format_response(result, "task_status")
        except Exception as e:
            self._handle_error(f"get task status for {upid}", e)

    def _get_task_log(self, node: str, upid: str) -> List[str]:
        """Get log entries for a task.

        Args:
            node: Node name where the task is running
            upid: Task UPID

        Returns:
            List of log entries
        """
        try:
            log_result = self.proxmox.nodes(node).tasks(upid).log.get()
            return [entry.get("t", "") for entry in log_result]
        except Exception:
            return []

    def cancel_task(self, upid: str) -> List[Content]:
        """Cancel a running task.

        Args:
            upid: Task UPID (Unique Process ID) to cancel

        Returns:
            List of Content objects containing operation result
        """
        try:
            # Parse node from UPID
            node = upid.split(':')[1]
            
            # Cancel the task
            result = self.proxmox.nodes(node).tasks(upid).delete()
            
            return self._format_response({
                "success": True,
                "upid": upid,
                "message": f"Task {upid} cancellation initiated"
            }, "task_cancel")
        except Exception as e:
            self._handle_error(f"cancel task {upid}", e)
