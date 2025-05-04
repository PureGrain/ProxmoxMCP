"""
Output templates for Proxmox MCP resource types.
"""
from typing import Dict, List, Any
from .formatters import ProxmoxFormatters
from .theme import ProxmoxTheme
from .colors import ProxmoxColors
from .components import ProxmoxComponents

class ProxmoxTemplates:
    """Output templates for different Proxmox resource types."""

    @staticmethod
    def node_list(nodes: List[Dict[str, Any]]) -> str:
        """Template for node list output.

        Args:
            nodes: List of node data dictionaries

        Returns:
            Formatted node list string
        """
        result = [f"{ProxmoxTheme.RESOURCES['node']} Proxmox Nodes"]

        for node in nodes:
            # Get node status
            status = node.get("status", "unknown")

            # Get memory info
            memory = node.get("memory", {})
            memory_used = memory.get("used", 0)
            memory_total = memory.get("total", 0)
            memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0

            # Format node info
            result.extend([
                "",  # Empty line between nodes
                f"{ProxmoxTheme.RESOURCES['node']} {node['node']}",
                f"  • Status: {status.upper()}",
                f"  • Uptime: {ProxmoxFormatters.format_uptime(node.get('uptime', 0))}",
                f"  • CPU Cores: {node.get('maxcpu', 'N/A')}",
                f"  • Memory: {ProxmoxFormatters.format_bytes(memory_used)} / "
                f"{ProxmoxFormatters.format_bytes(memory_total)} ({memory_percent:.1f}%)"
            ])

            # Add disk usage if available
            disk = node.get("disk", {})
            if disk:
                disk_used = disk.get("used", 0)
                disk_total = disk.get("total", 0)
                disk_percent = (disk_used / disk_total * 100) if disk_total > 0 else 0
                result.append(
                    f"  • Disk: {ProxmoxFormatters.format_bytes(disk_used)} / "
                    f"{ProxmoxFormatters.format_bytes(disk_total)} ({disk_percent:.1f}%)"
                )

        return "\n".join(result)

    @staticmethod
    def node_status(node: str, status: Dict[str, Any]) -> str:
        """Template for detailed node status output.

        Args:
            node: Node name
            status: Node status data

        Returns:
            Formatted node status string
        """
        memory = status.get("memory", {})
        memory_used = memory.get("used", 0)
        memory_total = memory.get("total", 0)
        memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0

        result = [
            f"{ProxmoxTheme.RESOURCES['node']} Node: {node}",
            f"  • Status: {status.get('status', 'unknown').upper()}",
            f"  • Uptime: {ProxmoxFormatters.format_uptime(status.get('uptime', 0))}",
            f"  • CPU Cores: {status.get('maxcpu', 'N/A')}",
            f"  • Memory: {ProxmoxFormatters.format_bytes(memory_used)} / "
            f"{ProxmoxFormatters.format_bytes(memory_total)} ({memory_percent:.1f}%)"
        ]

        # Add disk usage if available
        disk = status.get("disk", {})
        if disk:
            disk_used = disk.get("used", 0)
            disk_total = disk.get("total", 0)
            disk_percent = (disk_used / disk_total * 100) if disk_total > 0 else 0
            result.append(
                f"  • Disk: {ProxmoxFormatters.format_bytes(disk_used)} / "
                f"{ProxmoxFormatters.format_bytes(disk_total)} ({disk_percent:.1f}%)"
            )

        return "\n".join(result)

    @staticmethod
    def vm_list(vms: List[Dict[str, Any]]) -> str:
        """Template for VM list output.

        Args:
            vms: List of VM data dictionaries

        Returns:
            Formatted VM list string
        """
        result = [f"{ProxmoxTheme.RESOURCES['vm']} Virtual Machines"]

        for vm in vms:
            memory = vm.get("memory", {})
            memory_used = memory.get("used", 0)
            memory_total = memory.get("total", 0)
            memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0

            result.extend([
                "",  # Empty line between VMs
                f"{ProxmoxTheme.RESOURCES['vm']} {vm['name']} (ID: {vm['vmid']})",
                f"  • Status: {vm['status'].upper()}",
                f"  • Node: {vm['node']}",
                f"  • CPU Cores: {vm.get('cpus', 'N/A')}",
                f"  • Memory: {ProxmoxFormatters.format_bytes(memory_used)} / "
                f"{ProxmoxFormatters.format_bytes(memory_total)} ({memory_percent:.1f}%)"
            ])

        return "\n".join(result)

    @staticmethod
    def storage_list(storage: List[Dict[str, Any]]) -> str:
        """Template for storage list output.

        Args:
            storage: List of storage data dictionaries

        Returns:
            Formatted storage list string
        """
        result = [f"{ProxmoxTheme.RESOURCES['storage']} Storage Pools"]

        for store in storage:
            used = store.get("used", 0)
            total = store.get("total", 0)
            percent = (used / total * 100) if total > 0 else 0

            result.extend([
                "",  # Empty line between storage pools
                f"{ProxmoxTheme.RESOURCES['storage']} {store['storage']}",
                f"  • Status: {store.get('status', 'unknown').upper()}",
                f"  • Type: {store['type']}",
                f"  • Usage: {ProxmoxFormatters.format_bytes(used)} / "
                f"{ProxmoxFormatters.format_bytes(total)} ({percent:.1f}%)"
            ])

        return "\n".join(result)

    @staticmethod
    def container_list(containers: List[Dict[str, Any]]) -> str:
        """Template for container list output.

        Args:
            containers: List of container data dictionaries

        Returns:
            Formatted container list string
        """
        if not containers:
            return f"{ProxmoxTheme.RESOURCES['container']} No containers found"

        result = [f"{ProxmoxTheme.RESOURCES['container']} Containers"]

        for container in containers:
            memory = container.get("memory", {})
            memory_used = memory.get("used", 0)
            memory_total = memory.get("total", 0)
            memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0

            result.extend([
                "",  # Empty line between containers
                f"{ProxmoxTheme.RESOURCES['container']} {container['name']} (ID: {container['vmid']})",
                f"  • Status: {container['status'].upper()}",
                f"  • Node: {container['node']}",
                f"  • CPU Cores: {container.get('cpus', 'N/A')}",
                f"  • Memory: {ProxmoxFormatters.format_bytes(memory_used)} / "
                f"{ProxmoxFormatters.format_bytes(memory_total)} ({memory_percent:.1f}%)"
            ])

        return "\n".join(result)

    @staticmethod
    def container_status(container: Dict[str, Any]) -> str:
        """Template for container status output.

        Args:
            container: Container status data

        Returns:
            Formatted container status string
        """
        result = [f"{ProxmoxTheme.RESOURCES['container']} Container: {container.get('name', container.get('vmid', 'Unknown'))} (ID: {container['vmid']})"]

        # Basic container info
        result.extend([
            f"  • Status: {container.get('status', 'unknown').upper()}",
            f"  • Node: {container.get('node', 'N/A')}",
        ])

        # CPU info
        cpu = container.get('cpu', {})
        if isinstance(cpu, dict):
            result.append(f"  • CPU: {cpu.get('cores', 'N/A')} cores, {cpu.get('usage', 0) * 100:.1f}% usage")
        else:
            result.append(f"  • CPU: {container.get('cpus', 'N/A')} cores")

        # Memory info
        memory = container.get('memory', {})
        memory_used = memory.get('used', 0)
        memory_total = memory.get('total', 0)
        memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0
        result.append(f"  • Memory: {ProxmoxFormatters.format_bytes(memory_used)} / "
                     f"{ProxmoxFormatters.format_bytes(memory_total)} ({memory_percent:.1f}%)")

        # Uptime
        uptime = container.get('uptime', 0)
        if uptime > 0:
            result.append(f"  • Uptime: {ProxmoxFormatters.format_uptime(uptime)}")

        # Network info
        network = container.get('network', {})
        if network:
            result.append(f"  • Network: {ProxmoxFormatters.format_bytes(network.get('in_bytes', 0))} in, "
                         f"{ProxmoxFormatters.format_bytes(network.get('out_bytes', 0))} out")

        # Disk info
        disk = container.get('disk', {})
        if disk:
            result.append(f"  • Disk: {ProxmoxFormatters.format_bytes(disk.get('read_bytes', 0))} read, "
                         f"{ProxmoxFormatters.format_bytes(disk.get('write_bytes', 0))} write")

        return "\n".join(result)

    @staticmethod
    def container_config(config: Dict[str, Any]) -> str:
        """Template for container configuration output.

        Args:
            config: Container configuration data

        Returns:
            Formatted container configuration string
        """
        result = [f"{ProxmoxTheme.SECTIONS['configuration']} Container Configuration"]

        # Basic configuration
        result.extend([
            "",
            f"  • Hostname: {config.get('hostname', 'N/A')}",
            f"  • CPU: {config.get('cores', 'N/A')} cores",
            f"  • Memory: {config.get('memory', 'N/A')} MB",
            f"  • Swap: {config.get('swap', 'N/A')} MB",
            f"  • Start on boot: {'Yes' if config.get('onboot', 0) == 1 else 'No'}"
        ])

        # Network interfaces
        net_interfaces = []
        for key, value in config.items():
            if key.startswith('net') and key != 'netif':
                net_interfaces.append(f"  • {key}: {value}")

        if net_interfaces:
            result.append("")
            result.append(f"{ProxmoxTheme.SECTIONS['network']} Network Interfaces")
            result.extend(net_interfaces)

        # Storage/mount points
        mount_points = []
        for key, value in config.items():
            if key.startswith('mp') or key == 'rootfs':
                mount_points.append(f"  • {key}: {value}")

        if mount_points:
            result.append("")
            result.append(f"{ProxmoxTheme.SECTIONS['storage']} Storage")
            result.extend(mount_points)

        return "\n".join(result)

    @staticmethod
    def container_performance(performance: Dict[str, Any]) -> str:
        """Template for container performance output.

        Args:
            performance: Container performance data

        Returns:
            Formatted container performance string
        """
        result = [f"{ProxmoxTheme.SECTIONS['performance']} Container Performance"]

        # CPU usage
        result.append(f"  • CPU Usage: {performance.get('cpu_usage', 0) * 100:.1f}%")

        # Memory usage
        memory = performance.get('memory', {})
        memory_used = memory.get('used', 0)
        memory_total = memory.get('total', 0)
        memory_percent = (memory_used / memory_total * 100) if memory_total > 0 else 0
        result.append(f"  • Memory: {ProxmoxFormatters.format_bytes(memory_used)} / "
                     f"{ProxmoxFormatters.format_bytes(memory_total)} ({memory_percent:.1f}%)")

        # Disk I/O
        disk_io = performance.get('disk_io', {})
        result.append(f"  • Disk I/O: {ProxmoxFormatters.format_bytes(disk_io.get('read_bytes', 0))} read, "
                     f"{ProxmoxFormatters.format_bytes(disk_io.get('write_bytes', 0))} write")

        # Network I/O
        network = performance.get('network', {})
        result.append(f"  • Network I/O: {ProxmoxFormatters.format_bytes(network.get('in_bytes', 0))} in, "
                     f"{ProxmoxFormatters.format_bytes(network.get('out_bytes', 0))} out")

        return "\n".join(result)

    @staticmethod
    def container_templates(templates: List[Dict[str, Any]]) -> str:
        """Template for container templates output.

        Args:
            templates: List of container template data

        Returns:
            Formatted container templates string
        """
        if not templates:
            return f"{ProxmoxTheme.RESOURCES['template']} No container templates found"

        result = [f"{ProxmoxTheme.RESOURCES['template']} Container Templates"]

        for template in templates:
            volid = template.get('volid', 'Unknown')
            # Extract template name from volid (e.g., local:vztmpl/ubuntu-20.04-standard_20.04-1_amd64.tar.gz)
            template_name = volid.split('/')[-1] if '/' in volid else volid

            result.extend([
                "",  # Empty line between templates
                f"{ProxmoxTheme.RESOURCES['template']} {template_name}",
                f"  • Volume ID: {volid}",
                f"  • Size: {ProxmoxFormatters.format_bytes(template.get('size', 0))}",
                f"  • Format: {template.get('format', 'N/A')}"
            ])

        return "\n".join(result)

    @staticmethod
    def vm_templates(templates: List[Dict[str, Any]]) -> str:
        """Template for VM templates output.

        Args:
            templates: List of VM template data

        Returns:
            Formatted VM templates string
        """
        if not templates:
            return f"{ProxmoxTheme.RESOURCES['template']} No VM templates found"

        result = [f"{ProxmoxTheme.RESOURCES['template']} VM Templates"]

        for template in templates:
            template_name = template.get('name', f"vm-{template.get('vmid', 'Unknown')}")

            result.extend([
                "",  # Empty line between templates
                f"{ProxmoxTheme.RESOURCES['template']} {template_name} (ID: {template.get('vmid', 'Unknown')})",
                f"  • Node: {template.get('node', 'N/A')}",
                f"  • Description: {template.get('description', 'No description')}",
                f"  • CPU Cores: {template.get('cores', 'N/A')}",
                f"  • Memory: {template.get('memory', 'N/A')} MB",
                f"  • OS Type: {template.get('os_type', 'N/A')}"
            ])

            # Add disk information if available
            disks = template.get('disks', {})
            if disks:
                disk_info = []
                for disk_id, disk_value in disks.items():
                    disk_info.append(f"    - {disk_id}: {disk_value}")

                if disk_info:
                    result.append(f"  • Disks:")
                    result.extend(disk_info)

        return "\n".join(result)

    @staticmethod
    def template_details(template: Dict[str, Any]) -> str:
        """Template for detailed VM template information.

        Args:
            template: Template data dictionary

        Returns:
            Formatted template details string
        """
        if not template:
            return f"{ProxmoxTheme.RESOURCES['template']} Template details not found"

        template_name = template.get('name', f"vm-{template.get('vmid', 'Unknown')}")

        result = [
            f"{ProxmoxTheme.RESOURCES['template']} Template: {template_name} (ID: {template.get('vmid', 'Unknown')})",
            f"  • Node: {template.get('node', 'N/A')}",
            f"  • Description: {template.get('description', 'No description')}",
            f"  • CPU Cores: {template.get('cores', 'N/A')}",
            f"  • Memory: {template.get('memory', 'N/A')} MB",
            f"  • OS Type: {template.get('os_type', 'N/A')}"
        ]

        # Add disk information
        disks = template.get('disks', {})
        if disks:
            result.append("")
            result.append(f"{ProxmoxTheme.SECTIONS['storage']} Disks")
            for disk_id, disk_value in disks.items():
                result.append(f"  • {disk_id}: {disk_value}")

        # Add network information
        networks = template.get('networks', {})
        if networks:
            result.append("")
            result.append(f"{ProxmoxTheme.SECTIONS['network']} Network Interfaces")
            for net_id, net_value in networks.items():
                result.append(f"  • {net_id}: {net_value}")

        return "\n".join(result)

    @staticmethod
    def template_operation(operation: Dict[str, Any]) -> str:
        """Template for template operation output.

        Args:
            operation: Template operation result data

        Returns:
            Formatted template operation string
        """
        if operation.get('success', False):
            result = [
                f"{ProxmoxTheme.SECTIONS['success']} {operation.get('message', 'Operation completed successfully')}"
            ]

            # Add task ID if available
            if 'task_id' in operation:
                result.append("")
                result.append(f"Task ID: {operation.get('task_id', 'N/A')}")
        else:
            result = [
                f"{ProxmoxTheme.SECTIONS['error']} {operation.get('message', 'Operation failed')}"
            ]

            # Add error details if available
            if 'error' in operation:
                result.append("")
                result.append(f"Error: {operation.get('error', 'Unknown error')}")

        return "\n".join(result)

    @staticmethod
    def template_clone(clone_result: Dict[str, Any]) -> str:
        """Template for template clone operation output.

        Args:
            clone_result: Template clone operation result data

        Returns:
            Formatted template clone operation string
        """
        if clone_result.get('success', False):
            result = [
                f"{ProxmoxTheme.SECTIONS['success']} {clone_result.get('message', 'Template cloned successfully')}"
            ]

            # Add task ID if available
            if 'task_id' in clone_result:
                result.append("")
                result.append(f"Task ID: {clone_result.get('task_id', 'N/A')}")
        else:
            result = [
                f"{ProxmoxTheme.SECTIONS['error']} {clone_result.get('message', 'Template clone failed')}"
            ]

            # Add error details if available
            if 'error' in clone_result:
                result.append("")
                result.append(f"Error: {clone_result.get('error', 'Unknown error')}")

        return "\n".join(result)

    @staticmethod
    def container_operation(operation: Dict[str, Any]) -> str:
        """Template for container operation output.

        Args:
            operation: Container operation result data

        Returns:
            Formatted container operation string
        """
        if operation.get('success', False):
            result = [
                f"{ProxmoxTheme.SECTIONS['success']} {operation.get('message', 'Operation completed successfully')}",
                "",
                f"Task ID: {operation.get('task_id', 'N/A')}"
            ]
        else:
            result = [
                f"{ProxmoxTheme.SECTIONS['error']} {operation.get('message', 'Operation failed')}",
                "",
                f"Error: {operation.get('error', 'Unknown error')}"
            ]

        return "\n".join(result)

    @staticmethod
    def container_command(command_result: Dict[str, Any]) -> str:
        """Template for container command execution output.

        Args:
            command_result: Command execution result data

        Returns:
            Formatted command execution string
        """
        success = command_result.get('success', False)
        exit_code = command_result.get('exit_code', 1)
        output = command_result.get('output', '')

        if success:
            result = [
                f"{ProxmoxTheme.SECTIONS['success']} Command executed successfully (exit code: {exit_code})",
                "",
                "Output:",
                f"{output}"
            ]
        else:
            result = [
                f"{ProxmoxTheme.SECTIONS['error']} Command execution failed (exit code: {exit_code})",
                "",
                "Output:",
                f"{output}"
            ]

        return "\n".join(result)

    @staticmethod
    def container_clone(clone_result: Dict[str, Any]) -> str:
        """Template for container clone operation output.

        Args:
            clone_result: Container clone operation result data

        Returns:
            Formatted container clone operation string
        """
        if clone_result.get('success', False):
            result = [
                f"{ProxmoxTheme.SECTIONS['success']} {clone_result.get('message', 'Container cloned successfully')}",
                "",
                f"Task ID: {clone_result.get('task_id', 'N/A')}"
            ]
        else:
            result = [
                f"{ProxmoxTheme.SECTIONS['error']} {clone_result.get('message', 'Container clone failed')}",
                "",
                f"Error: {clone_result.get('error', 'Unknown error')}"
            ]

        return "\n".join(result)

    @staticmethod
    def cluster_status(status: Dict[str, Any]) -> str:
        """Template for cluster status output.

        Args:
            status: Cluster status data

        Returns:
            Formatted cluster status string
        """
        result = [f"{ProxmoxTheme.SECTIONS['configuration']} Proxmox Cluster"]

        # Basic cluster info
        result.extend([
            "",
            f"  • Name: {status.get('name', 'N/A')}",
            f"  • Quorum: {'OK' if status.get('quorum') else 'NOT OK'}",
            f"  • Nodes: {status.get('nodes', 0)}",
        ])

        # Add resource count if available
        resources = status.get('resources', [])
        if resources:
            result.append(f"  • Resources: {len(resources)}")

        return "\n".join(result)
