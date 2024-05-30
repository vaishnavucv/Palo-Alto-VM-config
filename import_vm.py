import subprocess
import os
import time

# Define paths and VM settings
ova_file_path = "/path/to/PA-VM-9.0.4.ova"
vm_name = "PA-VM-9.0.4"
ram_size = "5120"  # 5GiB in MB
cpu_count = "4"
host_only_adapter = "vboxnet0"

# Function to run a subprocess command
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with error: {result.stderr}")
    else:
        print(f"Command succeeded: {result.stdout}")
    return result

# Import the OVA file
print("Importing OVA file...")
import_command = f"/usr/bin/VBoxManage import {ova_file_path}"
run_command(import_command)

# Wait for the import to complete
time.sleep(5)

# Change VM settings
print("Changing VM settings...")

# Add host-only adapter
network_command = f"/usr/bin/VBoxManage modifyvm {vm_name} --nic1 hostonly --hostonlyadapter1 {host_only_adapter}"
run_command(network_command)

# Increase RAM size
ram_command = f"/usr/bin/VBoxManage modifyvm {vm_name} --memory {ram_size}"
run_command(ram_command)

# Increase number of processors
cpu_command = f"/usr/bin/VBoxManage modifyvm {vm_name} --cpus {cpu_count}"
run_command(cpu_command)

# Start the VM
print("Starting the VM...")
start_command = f"/usr/bin/VBoxManage startvm {vm_name} --type headless"
run_command(start_command)

print("VM setup and start completed successfully.")
