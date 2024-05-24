import subprocess
import paramiko
import time
import webbrowser

# Constants
VBOXMANAGE_PATH = '/usr/bin/VBoxManage'
VM_NAME = "PA-VM-9.0.4"
LOG_FILE = "log.txt"
SSH_IP = "192.168.56.100"
SSH_USERNAME = "admin"
SSH_PASSWORD = "Password123$"
DELAY_SECONDS = 15  

VM_COMMANDS = [
    "configure",
    "set deviceconfig system type static",
    "set deviceconfig system ip-address 192.168.56.100",
    "set deviceconfig system netmask 225.255.255.0",
    "set deviceconfig system default-gateway 192.168.56.1",
    "commit force",
    "exit"
]

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

def execute_ssh_commands(ip, username, password, commands):
    """ Execute multiple commands over SSH and log output """
    log_message(f"Attempting SSH connection to {ip}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)

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

def open_firefox(url):
    """ Open Firefox with a specified URL """
    log_message(f"Opening Firefox at {url}")
    webbrowser.get('firefox').open(url)

def main():
    log_running_vms()
    if not subprocess.run([VBOXMANAGE_PATH, 'list', 'runningvms'], stdout=subprocess.PIPE, text=True).stdout.startswith(f'"{VM_NAME}"'):
        log_message(f"VM {VM_NAME} is not running. Exiting the script.")
        return
    execute_ssh_commands(SSH_IP, SSH_USERNAME, SSH_PASSWORD, VM_COMMANDS)
    open_firefox("https://192.168.56.100")

if __name__ == "__main__":
    main()
