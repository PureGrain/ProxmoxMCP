#!/usr/bin/env python3
"""
Simple MCP server for Proxmox API.
This server implements the MCP protocol and uses the proxmox_api.py script to interact with the Proxmox API.
"""
import json
import logging
import os
import sys
import subprocess
import argparse
from typing import Dict, Any, Optional, List, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("simple_proxmox_mcp.log")
    ]
)
logger = logging.getLogger("simple-proxmox-mcp")

# Get the absolute path to the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")
API_SCRIPT_PATH = os.path.join(SCRIPT_DIR, "proxmox_api.py")

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json."""
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)

def run_proxmox_api(action: str, **kwargs) -> Dict[str, Any]:
    """Run the proxmox_api.py script with the specified action and arguments."""
    config = load_config()

    cmd = [
        sys.executable,
        API_SCRIPT_PATH,
        "--host", config["proxmox"]["host"],
        "--user", config["auth"]["user"],
        "--token-name", config["auth"]["token_name"],
        "--token-value", config["auth"]["token_value"],
        "--action", action
    ]

    # Add additional arguments
    for key, value in kwargs.items():
        if value is None:
            continue

        # Handle boolean flags differently
        if isinstance(value, bool):
            if value:
                cmd.append(f"--{key.replace('_', '-')}")
        else:
            cmd.extend([f"--{key.replace('_', '-')}", str(value)])

    try:
        logger.info(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}: {e.stderr}")
        return {"error": f"Command failed: {e.stderr}"}
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON output: {e}")
        return {"error": f"Failed to parse JSON output: {e}"}
    except Exception as e:
        logger.error(f"Error running command: {e}")
        return {"error": f"Error running command: {e}"}

def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle an MCP request."""
    try:
        tool_name = request.get("tool")
        arguments = request.get("arguments", {})

        # Basic operations
        if tool_name == "get_nodes":
            return run_proxmox_api("get_nodes")
        elif tool_name == "get_node_status":
            node = arguments.get("node")
            if not node:
                return {"error": "Node name is required for get_node_status"}
            return run_proxmox_api("get_node_status", node=node)
        elif tool_name == "get_vms":
            return run_proxmox_api("get_vms")
        elif tool_name == "execute_vm_command":
            node = arguments.get("node")
            vmid = arguments.get("vmid")
            command = arguments.get("command")
            if not node or not vmid or not command:
                return {"error": "Node name, VM ID, and command are required for execute_vm_command"}
            return run_proxmox_api("execute_vm_command", node=node, vmid=vmid, command=command)
        elif tool_name == "get_storage":
            return run_proxmox_api("get_storage")
        elif tool_name == "get_cluster_status":
            return run_proxmox_api("get_cluster_status")

        # Template operations
        elif tool_name == "get_templates":
            return run_proxmox_api("get_templates")
        elif tool_name == "clone_template":
            node = arguments.get("node")
            template_vmid = arguments.get("template_vmid")
            new_vm_name = arguments.get("new_vm_name")
            target_node = arguments.get("target_node")
            full_clone = arguments.get("full_clone", True)
            storage = arguments.get("storage")

            if not node or not template_vmid or not new_vm_name:
                return {"error": "Node name, template VM ID, and new VM name are required for clone_template"}

            return run_proxmox_api(
                "clone_template",
                node=node,
                vmid=template_vmid,
                new_vm_name=new_vm_name,
                target_node=target_node,
                full_clone=full_clone,
                storage=storage
            )

        # VM power operations
        elif tool_name == "start_vm":
            node = arguments.get("node")
            vmid = arguments.get("vmid")

            if not node or not vmid:
                return {"error": "Node name and VM ID are required for start_vm"}

            return run_proxmox_api("start_vm", node=node, vmid=vmid)
        elif tool_name == "stop_vm":
            node = arguments.get("node")
            vmid = arguments.get("vmid")

            if not node or not vmid:
                return {"error": "Node name and VM ID are required for stop_vm"}

            return run_proxmox_api("stop_vm", node=node, vmid=vmid)
        elif tool_name == "reboot_vm":
            node = arguments.get("node")
            vmid = arguments.get("vmid")

            if not node or not vmid:
                return {"error": "Node name and VM ID are required for reboot_vm"}

            return run_proxmox_api("reboot_vm", node=node, vmid=vmid)

        # VM configuration operations
        elif tool_name == "update_vm_config":
            node = arguments.get("node")
            vmid = arguments.get("vmid")
            cpu = arguments.get("cpu")
            memory = arguments.get("memory")
            name = arguments.get("name")
            description = arguments.get("description")

            if not node or not vmid:
                return {"error": "Node name and VM ID are required for update_vm_config"}

            return run_proxmox_api(
                "update_vm_config",
                node=node,
                vmid=vmid,
                cpu=cpu,
                memory=memory,
                name=name,
                description=description
            )
        elif tool_name == "get_vm_config":
            node = arguments.get("node")
            vmid = arguments.get("vmid")

            if not node or not vmid:
                return {"error": "Node name and VM ID are required for get_vm_config"}

            return run_proxmox_api("get_vm_config", node=node, vmid=vmid)

        # Task operations
        elif tool_name == "get_task_status":
            node = arguments.get("node")
            task_id = arguments.get("task_id")

            if not node or not task_id:
                return {"error": "Node name and task ID are required for get_task_status"}

            return run_proxmox_api("get_task_status", node=node, task_id=task_id)
        elif tool_name == "wait_for_task":
            node = arguments.get("node")
            task_id = arguments.get("task_id")
            timeout = arguments.get("timeout", 300)

            if not node or not task_id:
                return {"error": "Node name and task ID are required for wait_for_task"}

            return run_proxmox_api("wait_for_task", node=node, task_id=task_id, timeout=timeout)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    except Exception as e:
        logger.error(f"Error handling MCP request: {e}")
        return {"error": f"Error handling MCP request: {e}"}

def mcp_server_info() -> Dict[str, Any]:
    """Return information about the MCP server."""
    return {
        "name": "simple-proxmox-mcp",
        "version": "1.1.0",
        "description": "Simple MCP server for Proxmox API with VM management capabilities",
        "tools": [
            # Basic operations
            {
                "name": "get_nodes",
                "description": "List all nodes in the Proxmox cluster with their status, CPU, memory, and role information.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_node_status",
                "description": "Get detailed status information for a specific Proxmox node.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Name/ID of node to query (e.g. 'pve1', 'proxmox-node2')"
                        }
                    },
                    "required": ["node"]
                }
            },
            {
                "name": "get_vms",
                "description": "List all virtual machines across the cluster with their status and resource usage.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "execute_vm_command",
                "description": "Execute commands in a VM via QEMU guest agent.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Host node name (e.g. 'pve1', 'proxmox-node2')"
                        },
                        "vmid": {
                            "type": "string",
                            "description": "VM ID number (e.g. '100', '101')"
                        },
                        "command": {
                            "type": "string",
                            "description": "Shell command to run (e.g. 'uname -a', 'systemctl status nginx')"
                        }
                    },
                    "required": ["node", "vmid", "command"]
                }
            },
            {
                "name": "get_storage",
                "description": "List storage pools across the cluster with their usage and configuration.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_cluster_status",
                "description": "Get overall Proxmox cluster health and configuration status.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },

            # Template operations
            {
                "name": "get_templates",
                "description": "List all VM templates available across the cluster.",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "clone_template",
                "description": "Clone a VM template to create a new VM.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Node where the template is located"
                        },
                        "template_vmid": {
                            "type": "string",
                            "description": "VM ID of the template to clone"
                        },
                        "new_vm_name": {
                            "type": "string",
                            "description": "Name for the new VM"
                        },
                        "target_node": {
                            "type": "string",
                            "description": "Target node for the new VM (optional)"
                        },
                        "full_clone": {
                            "type": "boolean",
                            "description": "Whether to perform a full clone (true) or linked clone (false)"
                        },
                        "storage": {
                            "type": "string",
                            "description": "Storage for the new VM (optional)"
                        }
                    },
                    "required": ["node", "template_vmid", "new_vm_name"]
                }
            },

            # VM power operations
            {
                "name": "start_vm",
                "description": "Start a VM.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Node where the VM is located"
                        },
                        "vmid": {
                            "type": "string",
                            "description": "VM ID to start"
                        }
                    },
                    "required": ["node", "vmid"]
                }
            },
            {
                "name": "stop_vm",
                "description": "Shutdown a VM gracefully.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Node where the VM is located"
                        },
                        "vmid": {
                            "type": "string",
                            "description": "VM ID to shutdown"
                        }
                    },
                    "required": ["node", "vmid"]
                }
            },
            {
                "name": "reboot_vm",
                "description": "Reboot a VM gracefully.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Node where the VM is located"
                        },
                        "vmid": {
                            "type": "string",
                            "description": "VM ID to reboot"
                        }
                    },
                    "required": ["node", "vmid"]
                }
            },

            # VM configuration operations
            {
                "name": "update_vm_config",
                "description": "Update VM configuration (CPU, memory, name, description).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Node where the VM is located"
                        },
                        "vmid": {
                            "type": "string",
                            "description": "VM ID to update"
                        },
                        "cpu": {
                            "type": "integer",
                            "description": "Number of CPU cores"
                        },
                        "memory": {
                            "type": "integer",
                            "description": "Memory in MB"
                        },
                        "name": {
                            "type": "string",
                            "description": "New name for the VM"
                        },
                        "description": {
                            "type": "string",
                            "description": "Description for the VM"
                        }
                    },
                    "required": ["node", "vmid"]
                }
            },
            {
                "name": "get_vm_config",
                "description": "Get detailed VM configuration.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Node where the VM is located"
                        },
                        "vmid": {
                            "type": "string",
                            "description": "VM ID to query"
                        }
                    },
                    "required": ["node", "vmid"]
                }
            },

            # Task operations
            {
                "name": "get_task_status",
                "description": "Get the status of a task.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Node where the task is running"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "Task ID to query"
                        }
                    },
                    "required": ["node", "task_id"]
                }
            },
            {
                "name": "wait_for_task",
                "description": "Wait for a task to complete.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "node": {
                            "type": "string",
                            "description": "Node where the task is running"
                        },
                        "task_id": {
                            "type": "string",
                            "description": "Task ID to wait for"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Timeout in seconds (default: 300)"
                        }
                    },
                    "required": ["node", "task_id"]
                }
            }
        ]
    }

def main():
    """Main function to run the MCP server."""
    parser = argparse.ArgumentParser(description='Simple MCP server for Proxmox API')
    parser.add_argument('--tool', help='Tool to execute')
    parser.add_argument('--arguments', help='JSON-encoded arguments for the tool')
    parser.add_argument('--info', action='store_true', help='Print server information and exit')
    parser.add_argument('--once', action='store_true', help='Run once and exit')

    args = parser.parse_args()

    # Print server information and exit
    if args.info:
        print(json.dumps(mcp_server_info(), indent=2))
        return

    # Run a specific tool once and exit
    if args.tool:
        arguments = {}
        if args.arguments:
            try:
                arguments = json.loads(args.arguments)
            except json.JSONDecodeError as e:
                print(json.dumps({"error": f"Failed to parse arguments: {e}"}))
                sys.exit(1)

        result = handle_mcp_request({"tool": args.tool, "arguments": arguments})
        print(json.dumps(result, indent=2))
        return

    # Run the MCP server in interactive mode
    logger.info("Starting MCP server in interactive mode")
    print(json.dumps({"status": "ready", "server": mcp_server_info()}))
    sys.stdout.flush()

    try:
        while True:
            try:
                # Use a more robust way to read from stdin
                line = ""
                while True:
                    char = sys.stdin.read(1)
                    if not char:  # EOF
                        break
                    line += char
                    if char == '\n':
                        break

                if not line.strip():
                    continue

                logger.info(f"Received request: {line.strip()}")
                request = json.loads(line)
                response = handle_mcp_request(request)
                logger.info(f"Sending response: {json.dumps(response)}")
                print(json.dumps(response))
                sys.stdout.flush()

                if args.once:
                    logger.info("Exiting after one request (--once flag)")
                    break
            except json.JSONDecodeError as e:
                print(json.dumps({"error": f"Failed to parse request: {e}"}))
                sys.stdout.flush()
    except KeyboardInterrupt:
        logger.info("MCP server stopped by user")
    except Exception as e:
        logger.error(f"Error in MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()