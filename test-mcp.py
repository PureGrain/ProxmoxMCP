#!/usr/bin/env python3
"""
Simple test script for ProxmoxMCP server.
"""
import json
import subprocess
import sys

def main():
    """Run a simple test of the ProxmoxMCP server."""
    print("Testing ProxmoxMCP server...")
    
    # Test get_nodes tool
    cmd = [
        "/home/student/vscode/new-proxmox-mcp/ProxmoxMCP/.venv-py312/bin/python",
        "-m", "proxmox_mcp.server",
        "--tool", "get_nodes",
        "--once"
    ]
    
    env = {
        "PROXMOX_MCP_CONFIG": "/home/student/vscode/new-proxmox-mcp/ProxmoxMCP/proxmox-config/config.json"
    }
    
    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the JSON output
        output = result.stdout.strip()
        print("Raw output:", output)
        
        try:
            data = json.loads(output)
            print("\nParsed output:")
            print(json.dumps(data, indent=2))
            print("\nTest successful!")
            return 0
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON output")
            return 1
            
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return e.returncode

if __name__ == "__main__":
    sys.exit(main())