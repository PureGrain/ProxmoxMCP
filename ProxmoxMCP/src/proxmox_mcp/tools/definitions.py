"""
Tool descriptions for Proxmox MCP tools.
"""

# Template tool descriptions
GET_TEMPLATES_DESC = """Get all VM templates across the cluster with detailed information.

Example:
[{"vmid": "110", "name": "ubuntu-template", "node": "pve1", "description": "Ubuntu 22.04 Template", "cores": 2, "memory": 2048, "os_type": "l26"}]"""

CREATE_TEMPLATE_DESC = """Convert an existing VM into a template.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number to convert to template (e.g. '100')
name - Optional new name for the template
description - Optional description for the template

Example:
{"success": true, "message": "VM 100 successfully converted to template"}"""

CLONE_TEMPLATE_DESC = """Clone a VM template to create a new VM with advanced options.

Parameters:
node* - Source host node name (e.g. 'pve1')
template_vmid* - Template VM ID number (e.g. '100')
name* - Name for the new VM
target_node - Optional target node (defaults to source node)
target_vmid - Optional specific VM ID for the clone (system assigns if not specified)
target_storage - Optional target storage for the clone
full_clone - Whether to create a full clone (true) or linked clone (false) (default: true)
description - Optional description for the new VM

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmclone:100:root@pam:", "message": "Template 100 clone initiated with name 'new-vm'"}"""

UPDATE_TEMPLATE_DESC = """Update template properties.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Template VM ID number (e.g. '100')
name - Optional new name for the template
description - Optional new description for the template
cores - Optional number of CPU cores
memory - Optional memory in MB

Example:
{"success": true, "message": "Template 100 successfully updated"}"""

DELETE_TEMPLATE_DESC = """Delete a template.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Template VM ID number (e.g. '100')

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmdel:100:root@pam:", "message": "Template 100 deletion initiated"}"""

IMPORT_TEMPLATE_DESC = """Import a template from a URL.

Parameters:
node* - Host node name (e.g. 'pve1')
storage* - Storage to use for the template
url* - URL to download the template from
format - Optional format (e.g. 'qcow2', 'vmdk', 'raw')

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:download:100:root@pam:", "message": "Template import from https://example.com/template.qcow2 initiated"}"""

GET_TEMPLATE_DETAILS_DESC = """Get detailed information about a specific template.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Template VM ID number (e.g. '100')

Example:
{"vmid": "100", "node": "pve1", "name": "ubuntu-template", "description": "Ubuntu 22.04 Template", "cores": 2, "memory": 2048, "os_type": "l26", "disks": {"scsi0": "local-lvm:vm-100-disk-0"}, "networks": {"net0": "virtio=XX:XX:XX:XX:XX:XX,bridge=vmbr0"}}"""

# Node tool descriptions
GET_NODES_DESC = """List all nodes in the Proxmox cluster with their status, CPU, memory, and role information.

Example:
{"node": "pve1", "status": "online", "cpu_usage": 0.15, "memory": {"used": "8GB", "total": "32GB"}}"""

GET_NODE_STATUS_DESC = """Get detailed status information for a specific Proxmox node.

Parameters:
node* - Name/ID of node to query (e.g. 'pve1')

Example:
{"cpu": {"usage": 0.15}, "memory": {"used": "8GB", "total": "32GB"}}"""

# VM tool descriptions
GET_VMS_DESC = """List all virtual machines across the cluster with their status and resource usage.

Example:
{"vmid": "100", "name": "ubuntu", "status": "running", "cpu": 2, "memory": 4096}"""

EXECUTE_VM_COMMAND_DESC = """Execute commands in a VM via QEMU guest agent.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')
command* - Shell command to run (e.g. 'uname -a')

Example:
{"success": true, "output": "Linux vm1 5.4.0", "exit_code": 0}"""

# VM lifecycle tool descriptions
START_VM_DESC = """Start a virtual machine.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmstart:100:root@pam:", "message": "VM 100 start initiated"}"""

STOP_VM_DESC = """Stop a virtual machine.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmstop:100:root@pam:", "message": "VM 100 stop initiated"}"""

REBOOT_VM_DESC = """Reboot a virtual machine.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmreboot:100:root@pam:", "message": "VM 100 reboot initiated"}"""

CREATE_VM_SNAPSHOT_DESC = """Create a snapshot of a virtual machine.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')
name* - Snapshot name (e.g. 'pre-update')
description - Optional snapshot description

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmsnap:100:root@pam:", "message": "Snapshot 'pre-update' creation initiated for VM 100"}"""

LIST_VM_SNAPSHOTS_DESC = """List all snapshots for a virtual machine.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')

Example:
[{"name": "pre-update", "description": "Before system update", "creation_time": 1623456789, "parent": ""}]"""

RESTORE_VM_SNAPSHOT_DESC = """Restore a virtual machine from a snapshot.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')
snapshot_name* - Name of the snapshot to restore

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmrollback:100:root@pam:", "message": "VM 100 restore to snapshot 'pre-update' initiated"}"""

CLONE_VM_DESC = """Clone a virtual machine.

Parameters:
node* - Source host node name (e.g. 'pve1')
vmid* - Source VM ID number (e.g. '100')
target_vmid* - Target VM ID number for the clone
target_node - Optional target node (defaults to source node)
name - Optional name for the cloned VM

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmclone:100:root@pam:", "message": "VM 100 clone to 101 initiated"}"""

GET_VM_PERFORMANCE_DESC = """Get performance metrics for a virtual machine.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')

Example:
{"cpu_usage": 0.15, "memory": {"used": "2GB", "total": "4GB"}, "disk_io": {"read_bytes": 1024, "write_bytes": 2048}, "network": {"in_bytes": 1024, "out_bytes": 2048}}"""

# Container tool descriptions
GET_CONTAINERS_DESC = """List all LXC containers across the cluster with their status and configuration.

Example:
{"vmid": "200", "name": "nginx", "status": "running", "template": "ubuntu-20.04"}"""

GET_CONTAINER_STATUS_DESC = """Get detailed status information for a specific container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')

Example:
{"vmid": "200", "name": "nginx", "status": "running", "cpu": {"cores": 1, "usage": 0.05}, "memory": {"used": "256MB", "total": "512MB"}}"""

CREATE_CONTAINER_DESC = """Create a new container from a template.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')
template* - Template to use (e.g. 'local:vztmpl/ubuntu-20.04-standard_20.04-1_amd64.tar.gz')
storage* - Storage to use for container
hostname - Optional hostname for the container
memory - Memory in MB (default: 512)
cores - Number of CPU cores (default: 1)
password - Optional root password
net0 - Optional network configuration

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:vzstart:200:root@pam:", "message": "Container 200 creation initiated"}"""

START_CONTAINER_DESC = """Start a container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:vzstart:200:root@pam:", "message": "Container 200 start initiated"}"""

STOP_CONTAINER_DESC = """Stop a container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:vzstop:200:root@pam:", "message": "Container 200 stop initiated"}"""

RESTART_CONTAINER_DESC = """Restart a container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:vzrestart:200:root@pam:", "message": "Container 200 restart initiated"}"""

DELETE_CONTAINER_DESC = """Delete a container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:vzdestroy:200:root@pam:", "message": "Container 200 deletion initiated"}"""

CLONE_CONTAINER_DESC = """Clone a container.

Parameters:
node* - Source host node name (e.g. 'pve1')
vmid* - Source container ID number (e.g. '200')
target_vmid* - Target container ID number for the clone
target_node - Optional target node (defaults to source node)
name - Optional name for the cloned container

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:vzclone:200:root@pam:", "message": "Container 200 clone to 201 initiated"}"""

GET_CONTAINER_CONFIG_DESC = """Get detailed configuration for a container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')

Example:
{"hostname": "nginx", "cores": 1, "memory": 512, "swap": 512, "net0": "name=eth0,bridge=vmbr0,ip=dhcp"}"""

UPDATE_CONTAINER_CONFIG_DESC = """Update container configuration.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')
cores - Number of CPU cores
memory - Memory in MB
hostname - Container hostname
description - Container description
net0 - Network interface configuration
onboot - Start on boot (1 or 0)

Example:
{"success": true, "message": "Container 200 configuration updated"}"""

EXECUTE_CONTAINER_COMMAND_DESC = """Execute a command in a container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')
command* - Shell command to run (e.g. 'uname -a')

Example:
{"success": true, "output": "Linux container1 5.4.0", "exit_code": 0}"""

GET_CONTAINER_PERFORMANCE_DESC = """Get performance metrics for a container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Container ID number (e.g. '200')

Example:
{"cpu_usage": 0.05, "memory": {"used": "256MB", "total": "512MB"}, "disk_io": {"read_bytes": 1024, "write_bytes": 2048}, "network": {"in_bytes": 1024, "out_bytes": 2048}}"""

GET_CONTAINER_TEMPLATES_DESC = """Get available container templates.

Parameters:
node* - Host node name (e.g. 'pve1')
storage - Optional storage ID to filter templates

Example:
[{"volid": "local:vztmpl/ubuntu-20.04-standard_20.04-1_amd64.tar.gz", "size": 123456789, "format": "tgz"}]"""

# Storage tool descriptions
GET_STORAGE_DESC = """List storage pools across the cluster with their usage and configuration.

Example:
{"storage": "local-lvm", "type": "lvm", "used": "500GB", "total": "1TB"}"""

# Task tool descriptions
GET_TASKS_DESC = """List recent tasks across the cluster with their status.

Parameters:
limit - Maximum number of tasks to return (default: 50)
vmid - Optional VM ID to filter tasks for a specific VM
node - Optional node name to filter tasks for a specific node

Example:
[{"upid": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmstart:100:root@pam:", "type": "qmstart", "status": "running", "node": "pve1", "starttime": 1623456789, "user": "root@pam"}]"""

GET_TASK_STATUS_DESC = """Get detailed status for a specific task.

Parameters:
upid* - Task UPID (Unique Process ID) to query

Example:
{"upid": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmstart:100:root@pam:", "node": "pve1", "type": "qmstart", "status": "running", "progress": 50, "log": ["starting VM 100", "VM 100 started successfully"]}"""

CANCEL_TASK_DESC = """Cancel a running task.

Parameters:
upid* - Task UPID (Unique Process ID) to cancel

Example:
{"success": true, "upid": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmstart:100:root@pam:", "message": "Task UPID:pve1:00051234:1234ABC:61A1B2C3:qmstart:100:root@pam: cancellation initiated"}"""

# Backup tool descriptions
CREATE_BACKUP_DESC = """Create a backup of a VM or container.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - VM ID number (e.g. '100')
storage - Optional storage ID where to store the backup
compress - Optional compression algorithm (zstd, lzo, gzip)
mode - Backup mode (snapshot, suspend, stop) (default: snapshot)

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:vzdump:100:root@pam:", "message": "Backup of VM 100 initiated"}"""

LIST_BACKUPS_DESC = """List available backups.

Parameters:
storage - Optional storage ID to filter backups
vmid - Optional VM ID to filter backups

Example:
[{"filename": "vzdump-qemu-100-2023_06_01-12_00_00.vma.zst", "node": "pve1", "vmid": "100", "size": 10737418240, "timestamp": 1623456789, "format": "vma.zst"}]"""

RESTORE_BACKUP_DESC = """Restore a VM or container from a backup.

Parameters:
node* - Host node name (e.g. 'pve1')
vmid* - Original VM ID number
backup_id* - Backup volume ID to restore from
target_storage - Optional storage ID for restored VM
target_vmid - Optional new VM ID for the restored VM

Example:
{"success": true, "task_id": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmrestore:100:root@pam:", "message": "Restore of VM 100 from backup vzdump-qemu-100-2023_06_01-12_00_00.vma.zst initiated"}"""

GET_BACKUP_CONFIG_DESC = """Get backup schedule configuration for a node.

Parameters:
node* - Host node name (e.g. 'pve1')

Example:
{"schedule": "0 0 * * *", "storage": "local", "compress": "zstd", "mode": "snapshot"}"""

UPDATE_BACKUP_SCHEDULE_DESC = """Update backup schedule configuration for a node.

Parameters:
node* - Host node name (e.g. 'pve1')
schedule* - Dictionary containing schedule configuration

Example:
{"success": true, "message": "Backup schedule updated for node pve1"}"""

# Cluster tool descriptions
GET_CLUSTER_STATUS_DESC = """Get overall Proxmox cluster health and configuration status.

Example:
{"name": "proxmox", "quorum": "ok", "nodes": 3, "ha_status": "active"}"""
