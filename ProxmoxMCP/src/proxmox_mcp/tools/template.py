"""
Template management tools for Proxmox MCP.

This module provides enhanced tools for managing VM templates:
- Listing templates with detailed information
- Creating templates from existing VMs
- Cloning templates with advanced options
- Updating template properties
- Deleting templates
- Importing templates from URLs or local files
- Exporting templates

These tools enable comprehensive template management through the MCP interface,
providing essential functionality for systems administrators.
"""
from typing import Dict, List, Optional, Any
from mcp.types import TextContent as Content
from .base import ProxmoxTool

class TemplateTools(ProxmoxTool):
    """Tools for managing Proxmox VM templates.
    
    Provides functionality for:
    - Retrieving detailed template information
    - Creating templates from existing VMs
    - Cloning templates with advanced options
    - Updating template properties
    - Deleting templates
    - Importing templates from URLs or local files
    - Exporting templates
    
    Implements fallback mechanisms for scenarios where detailed
    template information might be temporarily unavailable.
    """

    def __init__(self, proxmox_api):
        """Initialize template tools.

        Args:
            proxmox_api: Initialized ProxmoxAPI instance
        """
        super().__init__(proxmox_api)

    def get_templates(self) -> List[Content]:
        """Get all VM templates across the cluster with detailed information.

        Returns:
            List of Content objects containing template information
        """
        try:
            # Get all nodes in the cluster
            nodes = self.proxmox.nodes.get()
            templates = []

            # Iterate through each node to find templates
            for node in nodes:
                node_name = node['node']
                try:
                    # Get all VMs on the node
                    node_vms = self.proxmox.nodes(node_name).qemu.get()
                    
                    # Filter for templates (template=1)
                    node_templates = [vm for vm in node_vms if vm.get('template') == 1]
                    
                    # Add node information to each template
                    for template in node_templates:
                        template['node'] = node_name
                        
                        # Get additional template details
                        try:
                            vmid = template.get('vmid')
                            if vmid:
                                # Get config for additional details
                                config = self.proxmox.nodes(node_name).qemu(vmid).config.get()
                                template['description'] = config.get('description', 'No description')
                                template['cores'] = config.get('cores', 'N/A')
                                template['memory'] = config.get('memory', 'N/A')
                                template['os_type'] = config.get('ostype', 'N/A')
                                
                                # Get disk information
                                disks = {}
                                for key, value in config.items():
                                    if key.startswith('scsi') or key.startswith('ide') or key.startswith('sata'):
                                        disks[key] = value
                                template['disks'] = disks
                        except Exception as e:
                            self.logger.warning(f"Could not get detailed info for template {vmid}: {e}")
                    
                    templates.extend(node_templates)
                except Exception as e:
                    self.logger.warning(f"Could not get templates for node {node_name}: {e}")
            
            return self._format_response(templates, "vm_templates")
        except Exception as e:
            self._handle_error("get templates", e)

    def create_template(self, node: str, vmid: str, name: Optional[str] = None, 
                       description: Optional[str] = None) -> List[Content]:
        """Convert an existing VM into a template.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: VM ID number to convert to template (e.g., '100', '101')
            name: Optional new name for the template
            description: Optional description for the template

        Returns:
            List of Content objects containing operation result
        """
        try:
            # First, ensure the VM is stopped
            vm_status = self.proxmox.nodes(node).qemu(vmid).status.current.get()
            if vm_status.get('status') != 'stopped':
                return self._format_response({
                    "success": False,
                    "message": f"VM {vmid} must be stopped before converting to template. Current status: {vm_status.get('status')}"
                }, "template_operation")
            
            # Update config to convert to template
            params = {"template": 1}
            
            # Add optional parameters if provided
            if name or description:
                # Get additional parameters in a separate request
                update_params = {}
                if name:
                    update_params["name"] = name
                if description:
                    update_params["description"] = description
                
                # Update VM config with name/description first
                self.proxmox.nodes(node).qemu(vmid).config.put(**update_params)
            
            # Convert to template
            self.proxmox.nodes(node).qemu(vmid).config.put(**params)
            
            return self._format_response({
                "success": True,
                "message": f"VM {vmid} successfully converted to template"
            }, "template_operation")
        except Exception as e:
            self._handle_error(f"create template from VM {vmid}", e)

    def clone_template(self, node: str, template_vmid: str, name: str, 
                      target_node: Optional[str] = None, 
                      target_vmid: Optional[str] = None,
                      target_storage: Optional[str] = None,
                      full_clone: bool = True,
                      description: Optional[str] = None) -> List[Content]:
        """Clone a VM template to create a new VM with advanced options.

        Args:
            node: Source host node name (e.g., 'pve1', 'proxmox-node2')
            template_vmid: Template VM ID number (e.g., '100', '101')
            name: Name for the new VM
            target_node: Optional target node (defaults to source node)
            target_vmid: Optional specific VM ID for the clone (system assigns if not specified)
            target_storage: Optional target storage for the clone
            full_clone: Whether to create a full clone (true) or linked clone (false)
            description: Optional description for the new VM

        Returns:
            List of Content objects containing operation result
        """
        try:
            # Prepare clone parameters
            params = {
                "name": name,
                "full": 1 if full_clone else 0
            }
            
            # Add optional parameters if provided
            if target_node:
                params["target"] = target_node
            if target_vmid:
                params["newid"] = target_vmid
            if target_storage:
                params["storage"] = target_storage
            
            # Clone the template
            result = self.proxmox.nodes(node).qemu(template_vmid).clone.post(**params)
            
            # Get the new VM ID from the result
            task_id = result
            
            # If description is provided, update it after cloning
            if description and target_vmid:
                try:
                    target_node_name = target_node if target_node else node
                    self.proxmox.nodes(target_node_name).qemu(target_vmid).config.put(description=description)
                except Exception as e:
                    self.logger.warning(f"Could not update description for cloned VM: {e}")
            
            return self._format_response({
                "success": True,
                "task_id": task_id,
                "message": f"Template {template_vmid} clone initiated with name '{name}'"
            }, "template_clone")
        except Exception as e:
            self._handle_error(f"clone template {template_vmid}", e)

    def update_template(self, node: str, vmid: str, name: Optional[str] = None,
                       description: Optional[str] = None, 
                       cores: Optional[int] = None,
                       memory: Optional[int] = None) -> List[Content]:
        """Update template properties.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Template VM ID number (e.g., '100', '101')
            name: Optional new name for the template
            description: Optional new description for the template
            cores: Optional number of CPU cores
            memory: Optional memory in MB

        Returns:
            List of Content objects containing operation result
        """
        try:
            # Verify this is actually a template
            vm_config = self.proxmox.nodes(node).qemu(vmid).config.get()
            if vm_config.get('template') != 1:
                return self._format_response({
                    "success": False,
                    "message": f"VM {vmid} is not a template"
                }, "template_operation")
            
            # Prepare update parameters
            params = {}
            if name:
                params["name"] = name
            if description:
                params["description"] = description
            if cores:
                params["cores"] = cores
            if memory:
                params["memory"] = memory
            
            # No parameters provided
            if not params:
                return self._format_response({
                    "success": False,
                    "message": "No update parameters provided"
                }, "template_operation")
            
            # Update template config
            self.proxmox.nodes(node).qemu(vmid).config.put(**params)
            
            return self._format_response({
                "success": True,
                "message": f"Template {vmid} successfully updated"
            }, "template_operation")
        except Exception as e:
            self._handle_error(f"update template {vmid}", e)

    def delete_template(self, node: str, vmid: str) -> List[Content]:
        """Delete a template.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Template VM ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing operation result
        """
        try:
            # Verify this is actually a template
            vm_config = self.proxmox.nodes(node).qemu(vmid).config.get()
            if vm_config.get('template') != 1:
                return self._format_response({
                    "success": False,
                    "message": f"VM {vmid} is not a template"
                }, "template_operation")
            
            # Delete the template
            result = self.proxmox.nodes(node).qemu(vmid).delete()
            
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Template {vmid} deletion initiated"
            }, "template_operation")
        except Exception as e:
            self._handle_error(f"delete template {vmid}", e)

    def import_template(self, node: str, storage: str, url: str, 
                       format: Optional[str] = None) -> List[Content]:
        """Import a template from a URL.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            storage: Storage to use for the template
            url: URL to download the template from
            format: Optional format (e.g., 'qcow2', 'vmdk', 'raw')

        Returns:
            List of Content objects containing operation result
        """
        try:
            # Prepare import parameters
            params = {
                "content": "vztmpl",
                "storage": storage,
                "url": url
            }
            
            # Add optional parameters if provided
            if format:
                params["format"] = format
            
            # Import the template
            result = self.proxmox.nodes(node).storage(storage).download_url.post(**params)
            
            return self._format_response({
                "success": True,
                "task_id": result,
                "message": f"Template import from {url} initiated"
            }, "template_operation")
        except Exception as e:
            self._handle_error(f"import template from {url}", e)

    def get_template_details(self, node: str, vmid: str) -> List[Content]:
        """Get detailed information about a specific template.

        Args:
            node: Host node name (e.g., 'pve1', 'proxmox-node2')
            vmid: Template VM ID number (e.g., '100', '101')

        Returns:
            List of Content objects containing template details
        """
        try:
            # Get basic VM information
            vm_info = self.proxmox.nodes(node).qemu(vmid).get()
            
            # Verify this is actually a template
            if vm_info.get('template') != 1:
                return self._format_response({
                    "success": False,
                    "message": f"VM {vmid} is not a template"
                }, "template_operation")
            
            # Get detailed configuration
            config = self.proxmox.nodes(node).qemu(vmid).config.get()
            
            # Combine information
            template_details = {
                "vmid": vmid,
                "node": node,
                "name": vm_info.get('name', f"vm-{vmid}"),
                "description": config.get('description', 'No description'),
                "cores": config.get('cores', 'N/A'),
                "memory": config.get('memory', 'N/A'),
                "os_type": config.get('ostype', 'N/A')
            }
            
            # Get disk information
            disks = {}
            for key, value in config.items():
                if key.startswith('scsi') or key.startswith('ide') or key.startswith('sata'):
                    disks[key] = value
            template_details['disks'] = disks
            
            # Get network information
            networks = {}
            for key, value in config.items():
                if key.startswith('net'):
                    networks[key] = value
            template_details['networks'] = networks
            
            return self._format_response(template_details, "template_details")
        except Exception as e:
            self._handle_error(f"get template details for {vmid}", e)
