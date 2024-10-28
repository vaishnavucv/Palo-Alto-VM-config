import subprocess
import os
import time
import sys

# Ensure required packages are installed
def install_packages():
    required_packages = ['requests', 'termcolor']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing required package: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_packages()

import requests
from termcolor import colored

# Define paths and VM settings
download_path = "/tmp/PA-VM-9.0.4.ova"
vm_name = "PA-VM-9.0.4"
ram_size = "5120"  # 5GiB in MB
cpu_count = "4"
host_only_adapter = "vboxnet0"

# Function to run a subprocess command
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(colored(f"Command failed with error: {result.stderr}", 'red'))
    else:
        print(colored(f"Command succeeded: {result.stdout}", 'green'))
    return result

# Download the OVA file
def download_ova(url, path):
    print(colored(f"Downloading OVA file from {url} to {path}...", 'cyan'))
    response = requests.get(url, stream=True)
    with open(path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(colored("Download completed.", 'green'))

# Remove existing VM if it exists
def remove_existing_vm(vm_name):
    print(colored(f"Checking if VM '{vm_name}' exists...", 'cyan'))
    result = run_command(f"/usr/bin/VBoxManage list vms")
    if vm_name in result.stdout:
        print(colored(f"VM '{vm_name}' found. Removing...", 'yellow'))
        run_command(f"/usr/bin/VBoxManage unregistervm {vm_name} --delete")
        print(colored(f"VM '{vm_name}' removed.", 'green'))
    else:
        print(colored(f"VM '{vm_name}' does not exist. No action needed.", 'cyan'))

# Stop all running VMs
def stop_all_vms():
    print(colored("Stopping all running VMs...", 'cyan'))
    result = run_command("/usr/bin/VBoxManage list runningvms")
    running_vms = [line.split('"')[1] for line in result.stdout.splitlines()]
    for vm in running_vms:
        print(colored(f"Stopping VM: {vm}", 'yellow'))
        run_command(f"/usr/bin/VBoxManage controlvm {vm} poweroff")
    print(colored("All running VMs stopped.", 'green'))

# ASCII countdown function
def countdown(minutes):
    seconds = minutes * 60
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        time_format = f"{mins:02}:{secs:02}"
        print(colored(time_format, 'magenta'), end="\r")
        time.sleep(1)
        seconds -= 1
    print(colored("Countdown completed!", 'green'))

# Main function
def main():
    # Get the OVA URL from the user
    ova_url = input(colored("Enter the OVA URL for downloading: ", 'cyan')).strip()

    # Stop all running VMs
    stop_all_vms()

    # Download the OVA file
    download_ova(ova_url, download_path)

    # Remove existing VM if it exists
    remove_existing_vm(vm_name)

    # Import the OVA file
    print(colored("Importing OVA file...", 'cyan'))
    import_command = f"/usr/bin/VBoxManage import {download_path}"
    run_command(import_command)

    # Wait for the import to complete
    time.sleep(5)

    # Change VM settings
    print(colored("Changing VM settings...", 'cyan'))

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
    print(colored("Starting the VM...", 'cyan'))
    start_command = f"/usr/bin/VBoxManage startvm {vm_name} --type headless"
    run_command(start_command)

    print(colored("VM setup and start completed successfully.", 'green'))

    # ASCII countdown for 25 minutes
    print(colored("Starting 25-minute countdown...", 'cyan'))
    countdown(25)

    # Delete the downloaded OVA file
    if os.path.exists(download_path):
        os.remove(download_path)
        print(colored(f"Deleted the OVA file: {download_path}", 'green'))
    else:
        print(colored(f"OVA file not found: {download_path}", 'red'))

# Execute main function
if __name__ == "__main__":
    main()
