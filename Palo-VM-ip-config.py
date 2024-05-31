import subprocess
import paramiko
import time
import webbrowser
import socket

VBOXMANAGE_PATH = '/usr/bin/VBoxManage'
VM_NAME = "PA-VM-9.0.4"
LOG_FILE = "log.txt"
PRIMARY_SSH_IP = "192.168.56.100"
SECONDARY_SSH_IP = "192.168.56.101"
SSH_PORT = 22
SSH_USERNAME = "admin"
SSH_PASSWORD = "password123$"
DELAY_SECONDS = 15

def log_message(message):
    """Log messages to the terminal and a log file."""
    print(message)
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")

def log_running_vms():
    """ Log the list of running VMs to a file and handle errors """
    try:
        output = subprocess.check_output([VBOXMANAGE_PATH, 'list', 'runningvms'])
        log_message("Logged running VMs.")
        log_message(output.decode())
    except subprocess.CalledProcessError as e:
        log_message(f"Failed to list running VMs: {e}")
    except Exception as e:
        log_message(f"An error occurred: {e}")

def is_port_open(ip, port):
    """ Check if a port is open on the given IP """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def generate_vm_commands(ip):
    """ Generate VM configuration commands based on the given IP """
    return [
        "configure",
        f"set deviceconfig system type static",
        f"set deviceconfig system ip-address {ip}",
        "set deviceconfig system netmask 255.255.255.0",
        "set deviceconfig system default-gateway 192.168.56.1",
        "commit force",
        "exit"
    ]

def execute_ssh_commands(ip, username, password):
    """ Execute multiple commands over SSH and log output """
    commands = generate_vm_commands(ip)
    if not is_port_open(ip, SSH_PORT):
        log_message(f"{ip} is not reachable on port {SSH_PORT}. Trying alternate IP...")
        ip = SECONDARY_SSH_IP
        if not is_port_open(ip, SSH_PORT):
            log_message(f"Alternate IP {ip} is also not reachable. Exiting.")
            return False
        else:
            commands = generate_vm_commands(ip)  # Regenerate commands for alternate IP

    log_message(f"Attempting SSH connection to {ip}...")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port=SSH_PORT, username=username, password=password, look_for_keys=False, allow_agent=False)
        log_message("SSH connection established. Starting interactive session...")

        remote_conn = client.invoke_shell()
        time.sleep(DELAY_SECONDS)

        for command in commands:
            log_message(f"Sending command: {command}")
            remote_conn.send(command + "\n")
            time.sleep(3)
            response = remote_conn.recv(65535).decode('utf-8')
            log_message(response)

        client.close()
        log_message("Session closed.")
        return True
    except Exception as e:
        log_message(f"Failed to connect to {ip}: {e}")
        return False

def open_firefox(url):
    """ Open Firefox with a specified URL """
    log_message(f"Opening Firefox at {url}")
    webbrowser.get('firefox').open(url)

def main():
    log_running_vms()
    if not subprocess.run([VBOXMANAGE_PATH, 'list', 'runningvms'], stdout=subprocess.PIPE, text=True).stdout.startswith(f'"{VM_NAME}"'):
        log_message(f"VM {VM_NAME} is not running. Exiting the script.")
        return
    successful = execute_ssh_commands(PRIMARY_SSH_IP, SSH_USERNAME, SSH_PASSWORD)
    if successful:
        open_firefox(f"https://{PRIMARY_SSH_IP if is_port_open(PRIMARY_SSH_IP, SSH_PORT) else SECONDARY_SSH_IP}")

if __name__ == "__main__":
    main()
