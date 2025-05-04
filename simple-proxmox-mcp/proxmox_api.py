#!/usr/bin/env python3
"""
Simple script to directly interact with the Proxmox API.
This script can be called with specific parameters to perform different operations.
"""
import json
import sys
import urllib3
import argparse
import time
from proxmoxer import ProxmoxAPI

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def connect_to_proxmox(host, user, token_name, token_value):
    """Connect to Proxmox API."""
    try:
        proxmox = ProxmoxAPI(
            host,
            user=user,
            token_name=token_name,
            token_value=token_value,
            verify_ssl=False
        )
        return proxmox
    except Exception as e:
        print(json.dumps({"error": f"Failed to connect to Proxmox API: {str(e)}"}))
        sys.exit(1)

def get_nodes(proxmox):
    """Get all nodes in the Proxmox cluster."""
    try:
        nodes = proxmox.nodes.get()
        return nodes
    except Exception as e:
        return {"error": f"Failed to get nodes: {str(e)}"}

def get_node_status(proxmox, node):
    """Get detailed status information for a specific Proxmox node."""
    try:
        status = proxmox.nodes(node).status.get()
        return status
    except Exception as e:
        return {"error": f"Failed to get status for node {node}: {str(e)}"}

def get_vms(proxmox):
    """Get all VMs across the cluster."""
    try:
        nodes = proxmox.nodes.get()
        vms = []
        vms_by_node = {}

        for node in nodes:
            node_name = node['node']
            try:
                node_vms = proxmox.nodes(node_name).qemu.get()
                vms.extend(node_vms)
                vms_by_node[node_name] = node_vms
            except Exception as e:
                print(json.dumps({"error": f"Failed to get VMs for node {node_name}: {str(e)}"}))

        # Count total VMs and running VMs
        total_vms = len(vms)
        running_vms = [vm for vm in vms if vm['status'] == 'running']
        total_running = len(running_vms)

        # Count VMs by node
        node_stats = {}
        for node_name, node_vms in vms_by_node.items():
            node_running = [vm for vm in node_vms if vm['status'] == 'running']
            node_stats[node_name] = {
                "total": len(node_vms),
                "running": len(node_running),
                "running_vms": [{"vmid": vm['vmid'], "name": vm['name'], "status": vm['status']} for vm in node_running]
            }

        return {
            "total_vms": total_vms,
            "total_running": total_running,
            "nodes": node_stats,
            "vms": vms
        }
    except Exception as e:
        return {"error": f"Failed to get VMs: {str(e)}"}

def execute_vm_command(proxmox, node, vmid, command):
    """Execute a command in a VM via QEMU guest agent."""
    try:
        result = proxmox.nodes(node).qemu(vmid).agent.exec.post(command=command)
        return result
    except Exception as e:
        return {"error": f"Failed to execute command in VM {vmid} on node {node}: {str(e)}"}

def get_storage(proxmox):
    """Get storage pools across the cluster."""
    try:
        storage = proxmox.storage.get()
        return storage
    except Exception as e:
        return {"error": f"Failed to get storage: {str(e)}"}

def get_cluster_status(proxmox):
    """Get overall Proxmox cluster health and configuration status."""
    try:
        status = proxmox.cluster.status.get()
        return status
    except Exception as e:
        return {"error": f"Failed to get cluster status: {str(e)}"}

def get_templates(proxmox):
    """Get all VM templates across the cluster."""
    try:
        nodes = proxmox.nodes.get()
        templates = []

        for node in nodes:
            node_name = node['node']
            try:
                node_vms = proxmox.nodes(node_name).qemu.get()
                # Filter for templates
                node_templates = [vm for vm in node_vms if vm.get('template') == 1]

                # Add node information to each template
                for template in node_templates:
                    template['node'] = node_name

                templates.extend(node_templates)
            except Exception as e:
                print(json.dumps({"error": f"Failed to get templates for node {node_name}: {str(e)}"}))

        return {
            "total_templates": len(templates),
            "templates": templates
        }
    except Exception as e:
        return {"error": f"Failed to get templates: {str(e)}"}

def clone_template(proxmox, node, template_vmid, new_vm_name, target_node=None, full_clone=True, storage=None):
    """Clone a VM template to create a new VM."""
    try:
        # Get the next available VM ID
        next_vmid = get_next_vmid(proxmox)

        # Prepare clone parameters
        clone_params = {
            'newid': next_vmid,
            'name': new_vm_name,
            'full': 1 if full_clone else 0,
        }

        # Add optional parameters if provided
        if target_node:
            clone_params['target'] = target_node
        if storage:
            clone_params['storage'] = storage

        # Submit clone task
        task_result = proxmox.nodes(node).qemu(template_vmid).clone.post(**clone_params)

        # Get task ID from result
        task_id = None
        if isinstance(task_result, dict) and 'data' in task_result:
            task_id = task_result['data']
        else:
            task_id = task_result

        # Return task information and new VM ID
        return {
            "success": True,
            "task_id": task_id,
            "new_vmid": next_vmid,
            "message": f"Started cloning template {template_vmid} to create new VM '{new_vm_name}' with ID {next_vmid}"
        }
    except Exception as e:
        return {"error": f"Failed to clone template {template_vmid} on node {node}: {str(e)}"}

def get_next_vmid(proxmox):
    """Get the next available VM ID."""
    try:
        next_id = proxmox.cluster.nextid.get()
        return next_id
    except Exception as e:
        # Fallback: Use a random ID in the typical range
        import random
        return random.randint(100, 999)

def start_vm(proxmox, node, vmid):
    """Start a VM."""
    try:
        result = proxmox.nodes(node).qemu(vmid).status.start.post()
        task_id = None
        if isinstance(result, dict):
            task_id = result.get('data')
        else:
            task_id = result

        return {
            "success": True,
            "task_id": task_id,
            "message": f"Started VM {vmid} on node {node}"
        }
    except Exception as e:
        return {"error": f"Failed to start VM {vmid} on node {node}: {str(e)}"}

def stop_vm(proxmox, node, vmid):
    """Stop a VM (shutdown)."""
    try:
        result = proxmox.nodes(node).qemu(vmid).status.shutdown.post()
        task_id = None
        if isinstance(result, dict):
            task_id = result.get('data')
        else:
            task_id = result

        return {
            "success": True,
            "task_id": task_id,
            "message": f"Shutting down VM {vmid} on node {node}"
        }
    except Exception as e:
        return {"error": f"Failed to shutdown VM {vmid} on node {node}: {str(e)}"}

def reboot_vm(proxmox, node, vmid):
    """Reboot a VM."""
    try:
        result = proxmox.nodes(node).qemu(vmid).status.reboot.post()
        task_id = None
        if isinstance(result, dict):
            task_id = result.get('data')
        else:
            task_id = result

        return {
            "success": True,
            "task_id": task_id,
            "message": f"Rebooting VM {vmid} on node {node}"
        }
    except Exception as e:
        return {"error": f"Failed to reboot VM {vmid} on node {node}: {str(e)}"}

def update_vm_config(proxmox, node, vmid, cpu=None, memory=None, name=None, description=None):
    """Update VM configuration (CPU, memory, name, description)."""
    try:
        config_params = {}

        if cpu is not None:
            config_params['cores'] = cpu
        if memory is not None:
            # Memory in MB
            config_params['memory'] = memory
        if name is not None:
            config_params['name'] = name
        if description is not None:
            config_params['description'] = description

        if not config_params:
            return {"error": "No configuration parameters provided"}

        # Apply the configuration changes
        proxmox.nodes(node).qemu(vmid).config.put(**config_params)

        return {
            "success": True,
            "message": f"Updated configuration for VM {vmid} on node {node}",
            "updated_params": config_params
        }
    except Exception as e:
        return {"error": f"Failed to update VM {vmid} configuration on node {node}: {str(e)}"}

def get_vm_config(proxmox, node, vmid):
    """Get detailed VM configuration."""
    try:
        config = proxmox.nodes(node).qemu(vmid).config.get()
        return config
    except Exception as e:
        return {"error": f"Failed to get configuration for VM {vmid} on node {node}: {str(e)}"}

def get_task_status(proxmox, node, task_id):
    """Get the status of a task."""
    try:
        status = proxmox.nodes(node).tasks(task_id).status.get()
        return status
    except Exception as e:
        return {"error": f"Failed to get status for task {task_id} on node {node}: {str(e)}"}

def wait_for_task(proxmox, node, task_id, timeout=300, interval=2):
    """Wait for a task to complete."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            status = proxmox.nodes(node).tasks(task_id).status.get()
            if status.get('status') == 'stopped':
                return {
                    "success": status.get('exitstatus') == 'OK',
                    "status": status
                }
            time.sleep(interval)
        except Exception as e:
            return {"error": f"Error checking task status: {str(e)}"}

    return {"error": f"Task {task_id} did not complete within {timeout} seconds"}

def main():
    """Main function to parse arguments and call the appropriate function."""
    parser = argparse.ArgumentParser(description='Interact with Proxmox API')
    parser.add_argument('--host', required=True, help='Proxmox host')
    parser.add_argument('--user', required=True, help='Proxmox user')
    parser.add_argument('--token-name', required=True, help='Proxmox API token name')
    parser.add_argument('--token-value', required=True, help='Proxmox API token value')
    parser.add_argument('--action', required=True,
                        choices=['get_nodes', 'get_node_status', 'get_vms',
                                'execute_vm_command', 'get_storage', 'get_cluster_status',
                                'get_templates', 'clone_template', 'start_vm', 'stop_vm',
                                'reboot_vm', 'update_vm_config', 'get_vm_config',
                                'get_task_status', 'wait_for_task'],
                        help='Action to perform')

    # Common parameters
    parser.add_argument('--node', help='Node name (required for node-specific operations)')
    parser.add_argument('--vmid', help='VM ID (required for VM-specific operations)')

    # Parameters for execute_vm_command
    parser.add_argument('--command', help='Command to execute (required for execute_vm_command)')

    # Parameters for clone_template
    parser.add_argument('--new-vm-name', help='Name for the new VM (required for clone_template)')
    parser.add_argument('--target-node', help='Target node for the new VM (optional for clone_template)')
    parser.add_argument('--full-clone', action='store_true', help='Perform a full clone (optional for clone_template)')
    parser.add_argument('--storage', help='Storage for the new VM (optional for clone_template)')

    # Parameters for update_vm_config
    parser.add_argument('--cpu', type=int, help='Number of CPU cores (for update_vm_config)')
    parser.add_argument('--memory', type=int, help='Memory in MB (for update_vm_config)')
    parser.add_argument('--name', help='New name for the VM (for update_vm_config)')
    parser.add_argument('--description', help='Description for the VM (for update_vm_config)')

    # Parameters for get_task_status and wait_for_task
    parser.add_argument('--task-id', help='Task ID (required for task-related operations)')
    parser.add_argument('--timeout', type=int, default=300, help='Timeout in seconds (for wait_for_task)')

    args = parser.parse_args()

    # Connect to Proxmox
    proxmox = connect_to_proxmox(args.host, args.user, args.token_name, args.token_value)

    # Perform the requested action
    result = None

    # Basic operations
    if args.action == 'get_nodes':
        result = get_nodes(proxmox)
    elif args.action == 'get_node_status':
        if not args.node:
            print(json.dumps({"error": "Node name is required for get_node_status"}))
            sys.exit(1)
        result = get_node_status(proxmox, args.node)
    elif args.action == 'get_vms':
        result = get_vms(proxmox)
    elif args.action == 'execute_vm_command':
        if not args.node or not args.vmid or not args.command:
            print(json.dumps({"error": "Node name, VM ID, and command are required for execute_vm_command"}))
            sys.exit(1)
        result = execute_vm_command(proxmox, args.node, args.vmid, args.command)
    elif args.action == 'get_storage':
        result = get_storage(proxmox)
    elif args.action == 'get_cluster_status':
        result = get_cluster_status(proxmox)

    # Template operations
    elif args.action == 'get_templates':
        result = get_templates(proxmox)
    elif args.action == 'clone_template':
        if not args.node or not args.vmid or not args.new_vm_name:
            print(json.dumps({"error": "Node name, template VM ID, and new VM name are required for clone_template"}))
            sys.exit(1)
        result = clone_template(
            proxmox,
            args.node,
            args.vmid,
            args.new_vm_name,
            args.target_node,
            args.full_clone,
            args.storage
        )

    # VM power operations
    elif args.action == 'start_vm':
        if not args.node or not args.vmid:
            print(json.dumps({"error": "Node name and VM ID are required for start_vm"}))
            sys.exit(1)
        result = start_vm(proxmox, args.node, args.vmid)
    elif args.action == 'stop_vm':
        if not args.node or not args.vmid:
            print(json.dumps({"error": "Node name and VM ID are required for stop_vm"}))
            sys.exit(1)
        result = stop_vm(proxmox, args.node, args.vmid)
    elif args.action == 'reboot_vm':
        if not args.node or not args.vmid:
            print(json.dumps({"error": "Node name and VM ID are required for reboot_vm"}))
            sys.exit(1)
        result = reboot_vm(proxmox, args.node, args.vmid)

    # VM configuration operations
    elif args.action == 'update_vm_config':
        if not args.node or not args.vmid:
            print(json.dumps({"error": "Node name and VM ID are required for update_vm_config"}))
            sys.exit(1)
        result = update_vm_config(
            proxmox,
            args.node,
            args.vmid,
            args.cpu,
            args.memory,
            args.name,
            args.description
        )
    elif args.action == 'get_vm_config':
        if not args.node or not args.vmid:
            print(json.dumps({"error": "Node name and VM ID are required for get_vm_config"}))
            sys.exit(1)
        result = get_vm_config(proxmox, args.node, args.vmid)

    # Task operations
    elif args.action == 'get_task_status':
        if not args.node or not args.task_id:
            print(json.dumps({"error": "Node name and task ID are required for get_task_status"}))
            sys.exit(1)
        result = get_task_status(proxmox, args.node, args.task_id)
    elif args.action == 'wait_for_task':
        if not args.node or not args.task_id:
            print(json.dumps({"error": "Node name and task ID are required for wait_for_task"}))
            sys.exit(1)
        result = wait_for_task(proxmox, args.node, args.task_id, args.timeout)

    # Print the result as JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()