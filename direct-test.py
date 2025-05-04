#!/usr/bin/env python3
"""
Simple script to directly test the Proxmox API connection.
"""
import json
import sys
import urllib3
import warnings
from proxmoxer import ProxmoxAPI

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    """Test direct connection to Proxmox API."""
    print("Testing direct connection to Proxmox API...")
    
    # Connection details
    host = "12.12.8.100"
    user = "root@pam"
    token_name = "vscode-devops"
    token_value = "742a3d18-f2b5-4a07-9d92-6c30ac417b09"
    
    try:
        # Connect to Proxmox
        proxmox = ProxmoxAPI(
            host,
            user=user,
            token_name=token_name,
            token_value=token_value,
            verify_ssl=False
        )
        
        print(f"Successfully connected to Proxmox API at {host}")
        
        # Test getting nodes
        print("\nGetting nodes:")
        nodes = proxmox.nodes.get()
        print(json.dumps(nodes, indent=2))
        
        # Test getting VMs
        print("\nGetting VMs:")
        vms = []
        vms_by_node = {}
        for node in nodes:
            node_name = node['node']
            print(f"Getting VMs for node {node_name}")
            try:
                node_vms = proxmox.nodes(node_name).qemu.get()
                vms.extend(node_vms)
                vms_by_node[node_name] = node_vms
            except Exception as e:
                print(f"Error getting VMs for node {node_name}: {e}")
        
        # Count VMs across the cluster
        total_vms = len(vms)
        running_vms = [vm for vm in vms if vm['status'] == 'running']
        total_running = len(running_vms)
        
        print(f"\nTotal VMs across the cluster: {total_vms}")
        print(f"Total running VMs across the cluster: {total_running}")
        
        # Count VMs by node
        for node_name, node_vms in vms_by_node.items():
            node_running = [vm for vm in node_vms if vm['status'] == 'running']
            print(f"\nNode {node_name}: {len(node_vms)} VMs, {len(node_running)} running")
            print(f"Running VMs on {node_name}:")
            for vm in node_running:
                print(f"  - {vm['vmid']}: {vm['name']} (Status: {vm['status']})")
        
        print("\nAll VMs:")
        print(json.dumps(vms, indent=2))
        
        # Test getting storage
        print("\nGetting storage:")
        storage = proxmox.storage.get()
        print(json.dumps(storage, indent=2))
        
        print("\nAll tests completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())