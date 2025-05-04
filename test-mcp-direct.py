#!/usr/bin/env python3
"""
Simple script to test the ProxmoxMCP server directly using subprocess.
"""
import json
import subprocess
import sys
import urllib3
import warnings

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_mcp_tool(tool_name, arguments=None):
    """Run an MCP tool and return the result."""
    if arguments is None:
        arguments = {}
        
    cmd = [
        "/home/student/vscode/new-proxmox-mcp/ProxmoxMCP/.venv-py312/bin/python",
        "-m", "proxmox_mcp.server",
        "--tool", tool_name,
        "--once"
    ]
    
    if arguments:
        cmd.extend(["--arguments", json.dumps(arguments)])
    
    env = {
        "PROXMOX_MCP_CONFIG": "/home/student/vscode/new-proxmox-mcp/ProxmoxMCP/proxmox-config/config.json"
    }
    
    print(f"Running command: {' '.join(cmd)}")
    print(f"With arguments: {arguments}")
    
    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        
        output = result.stdout.strip()
        print(f"Raw output: {output}")
        
        try:
            data = json.loads(output)
            return data
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON output")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None

def main():
    """Test the ProxmoxMCP server."""
    print("Testing ProxmoxMCP server...")
    
    # Test get_nodes
    print("\n=== Testing get_nodes ===")
    nodes = run_mcp_tool("get_nodes")
    if nodes:
        print(json.dumps(nodes, indent=2))
    
    # Test get_node_status
    if nodes and len(nodes) > 0:
        node_name = nodes[0]["node"]
        print(f"\n=== Testing get_node_status for {node_name} ===")
        node_status = run_mcp_tool("get_node_status", {"node": node_name})
        if node_status:
            print(json.dumps(node_status, indent=2))
    
    # Test get_cluster_status
    print("\n=== Testing get_cluster_status ===")
    cluster_status = run_mcp_tool("get_cluster_status")
    if cluster_status:
        print(json.dumps(cluster_status, indent=2))
    
    # Test get_storage
    print("\n=== Testing get_storage ===")
    storage = run_mcp_tool("get_storage")
    if storage:
        print(json.dumps(storage, indent=2))
    
    print("\nTests completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())