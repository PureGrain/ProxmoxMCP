# ProxmoxMCP Tools Documentation

This document provides detailed information about the tools available in ProxmoxMCP.

## Basic Operations

### get_nodes

Lists all nodes in the Proxmox cluster with their status, CPU, memory, and role information.

**Parameters**: None

**Example**:
```bash
./manage-server.sh run get_nodes
```

### get_node_status

Gets detailed status information for a specific Proxmox node.

**Parameters**:
- `node` (string): The name of the node to get status for

**Example**:
```bash
./manage-server.sh run get_node_status '{"node": "pve-host01"}'
```

### get_vms

Lists all virtual machines across the cluster with their status and resource usage.

**Parameters**: None

**Example**:
```bash
./manage-server.sh run get_vms
```

### execute_vm_command

Executes commands in a VM via QEMU guest agent.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM
- `command` (string): The command to execute

**Example**:
```bash
./manage-server.sh run execute_vm_command '{"node": "pve-host01", "vmid": "100", "command": "uname -a"}'
```

### get_storage

Lists storage pools across the cluster with their usage and configuration.

**Parameters**: None

**Example**:
```bash
./manage-server.sh run get_storage
```

### get_cluster_status

Gets overall Proxmox cluster health and configuration status.

**Parameters**: None

**Example**:
```bash
./manage-server.sh run get_cluster_status
```

## Container Management

### get_containers

Lists all LXC containers across the cluster with their status and configuration.

**Parameters**: None

**Example**:
```bash
./manage-server.sh run get_containers
```

### get_container_status

Gets detailed status information for a specific container.

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container

**Example**:
```bash
./manage-server.sh run get_container_status '{"node": "pve-host01", "vmid": "200"}'
```

### create_container

Creates a new container from a template.

**Parameters**:
- `node` (string): The name of the node to create the container on
- `vmid` (string): The ID for the new container
- `template` (string): The template to use
- `storage` (string): The storage to use
- `hostname` (string): The hostname for the container
- `memory` (integer): The amount of memory in MB
- `cores` (integer): The number of CPU cores

**Example**:
```bash
./manage-server.sh run create_container '{"node": "pve-host01", "vmid": "200", "template": "local:vztmpl/ubuntu-20.04-standard_20.04-1_amd64.tar.gz", "storage": "local", "hostname": "container1", "memory": 512, "cores": 1}'
```

### start_container

Starts a container.

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container

**Example**:
```bash
./manage-server.sh run start_container '{"node": "pve-host01", "vmid": "200"}'
```

### stop_container

Stops a container.

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container

**Example**:
```bash
./manage-server.sh run stop_container '{"node": "pve-host01", "vmid": "200"}'
```

### restart_container

Restarts a container.

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container

**Example**:
```bash
./manage-server.sh run restart_container '{"node": "pve-host01", "vmid": "200"}'
```

### delete_container

Deletes a container.

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container

**Example**:
```bash
./manage-server.sh run delete_container '{"node": "pve-host01", "vmid": "200"}'
```

### clone_container

Clones an existing container.

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container to clone
- `target_vmid` (string): The ID for the new container
- `name` (string): The name for the new container

**Example**:
```bash
./manage-server.sh run clone_container '{"node": "pve-host01", "vmid": "200", "target_vmid": "201", "name": "container2"}'
```

### get_container_config

Gets detailed configuration for a container.

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container

**Example**:
```bash
./manage-server.sh run get_container_config '{"node": "pve-host01", "vmid": "200"}'
```

### update_container_config

Updates container configuration (CPU, memory, etc.).

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container
- `cores` (integer): The number of CPU cores
- `memory` (integer): The amount of memory in MB
- `hostname` (string): The hostname for the container

**Example**:
```bash
./manage-server.sh run update_container_config '{"node": "pve-host01", "vmid": "200", "cores": 2, "memory": 1024, "hostname": "updated-container"}'
```

### execute_container_command

Executes commands inside a container.

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container
- `command` (string): The command to execute

**Example**:
```bash
./manage-server.sh run execute_container_command '{"node": "pve-host01", "vmid": "200", "command": "uname -a"}'
```

### get_container_performance

Gets performance metrics for a container.

**Parameters**:
- `node` (string): The name of the node hosting the container
- `vmid` (string): The ID of the container

**Example**:
```bash
./manage-server.sh run get_container_performance '{"node": "pve-host01", "vmid": "200"}'
```

### get_container_templates

Gets available container templates.

**Parameters**:
- `node` (string): The name of the node to get templates from
- `storage` (string): The storage to get templates from

**Example**:
```bash
./manage-server.sh run get_container_templates '{"node": "pve-host01", "storage": "local"}'
```

## VM Lifecycle Management

### start_vm

Starts a virtual machine.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM

**Example**:
```bash
./manage-server.sh run start_vm '{"node": "pve-host01", "vmid": "100"}'
```

### stop_vm

Stops a virtual machine.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM

**Example**:
```bash
./manage-server.sh run stop_vm '{"node": "pve-host01", "vmid": "100"}'
```

### reboot_vm

Reboots a virtual machine.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM

**Example**:
```bash
./manage-server.sh run reboot_vm '{"node": "pve-host01", "vmid": "100"}'
```

### create_vm_snapshot

Creates a snapshot of a virtual machine.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM
- `name` (string): The name for the snapshot
- `description` (string): The description for the snapshot

**Example**:
```bash
./manage-server.sh run create_vm_snapshot '{"node": "pve-host01", "vmid": "100", "name": "pre-update", "description": "Before system update"}'
```

### list_vm_snapshots

Lists all snapshots for a virtual machine.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM

**Example**:
```bash
./manage-server.sh run list_vm_snapshots '{"node": "pve-host01", "vmid": "100"}'
```

### restore_vm_snapshot

Restores a virtual machine from a snapshot.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM
- `snapshot_name` (string): The name of the snapshot to restore

**Example**:
```bash
./manage-server.sh run restore_vm_snapshot '{"node": "pve-host01", "vmid": "100", "snapshot_name": "pre-update"}'
```

### clone_vm

Clones a virtual machine.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM to clone
- `target_vmid` (string): The ID for the new VM
- `name` (string): The name for the new VM

**Example**:
```bash
./manage-server.sh run clone_vm '{"node": "pve-host01", "vmid": "100", "target_vmid": "101", "name": "cloned-vm"}'
```

### get_vm_performance

Gets performance metrics for a virtual machine.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM

**Example**:
```bash
./manage-server.sh run get_vm_performance '{"node": "pve-host01", "vmid": "100"}'
```

## Task Management

### get_tasks

Lists recent tasks across the cluster with their status.

**Parameters**:
- `limit` (integer, optional): The maximum number of tasks to return

**Example**:
```bash
./manage-server.sh run get_tasks '{"limit": 10}'
```

### get_task_status

Gets detailed status for a specific task.

**Parameters**:
- `upid` (string): The UPID of the task

**Example**:
```bash
./manage-server.sh run get_task_status '{"upid": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmstart:100:root@pam:"}'
```

### cancel_task

Cancels a running task.

**Parameters**:
- `upid` (string): The UPID of the task

**Example**:
```bash
./manage-server.sh run cancel_task '{"upid": "UPID:pve1:00051234:1234ABC:61A1B2C3:qmstart:100:root@pam:"}'
```

## Backup Management

### create_backup

Creates a backup of a VM or container.

**Parameters**:
- `node` (string): The name of the node hosting the VM or container
- `vmid` (string): The ID of the VM or container
- `storage` (string): The storage to store the backup
- `compress` (string): The compression algorithm to use
- `mode` (string): The backup mode

**Example**:
```bash
./manage-server.sh run create_backup '{"node": "pve-host01", "vmid": "100", "storage": "local", "compress": "zstd", "mode": "snapshot"}'
```

### list_backups

Lists available backups.

**Parameters**:
- `storage` (string): The storage to list backups from

**Example**:
```bash
./manage-server.sh run list_backups '{"storage": "local"}'
```

### restore_backup

Restores a VM or container from a backup.

**Parameters**:
- `node` (string): The name of the node to restore to
- `vmid` (string): The ID of the VM or container
- `backup_id` (string): The ID of the backup to restore from

**Example**:
```bash
./manage-server.sh run restore_backup '{"node": "pve-host01", "vmid": "100", "backup_id": "local:backup/vzdump-qemu-100-2023_06_01-12_00_00.vma.zst"}'
```

### get_backup_config

Gets backup schedule configuration for a node.

**Parameters**:
- `node` (string): The name of the node to get backup configuration for

**Example**:
```bash
./manage-server.sh run get_backup_config '{"node": "pve-host01"}'
```

### update_backup_schedule

Updates backup schedule configuration for a node.

**Parameters**:
- `node` (string): The name of the node to update backup configuration for
- `schedule` (object): The backup schedule configuration

**Example**:
```bash
./manage-server.sh run update_backup_schedule '{"node": "pve-host01", "schedule": {"schedule": "0 0 * * *", "storage": "local", "compress": "zstd", "mode": "snapshot"}}'
```

## Template Operations

### get_templates

Lists all VM templates available across the cluster.

**Parameters**: None

**Example**:
```bash
./manage-server.sh run get_templates
```

### clone_template

Clones a VM template to create a new VM.

**Parameters**:
- `node` (string): The name of the node hosting the template
- `template_vmid` (string): The ID of the template
- `new_vm_name` (string): The name for the new VM
- `full_clone` (boolean): Whether to create a full clone

**Example**:
```bash
./manage-server.sh run clone_template '{"node": "pve-host01", "template_vmid": "110", "new_vm_name": "test-vm-from-template", "full_clone": true}'
```

## VM Configuration Operations

### update_vm_config

Updates VM configuration (CPU, memory, name, description).

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM
- `cpu` (integer): The number of CPU cores
- `memory` (integer): The amount of memory in MB
- `description` (string): The description for the VM

**Example**:
```bash
./manage-server.sh run update_vm_config '{"node": "pve-host01", "vmid": "109", "cpu": 2, "memory": 4096, "description": "Test VM created from template"}'
```

### get_vm_config

Gets detailed VM configuration.

**Parameters**:
- `node` (string): The name of the node hosting the VM
- `vmid` (string): The ID of the VM

**Example**:
```bash
./manage-server.sh run get_vm_config '{"node": "pve-host01", "vmid": "109"}'
```
