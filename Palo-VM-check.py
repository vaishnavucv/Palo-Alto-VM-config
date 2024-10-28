#!/bin/python3
#author : Vaihsnavu c v | vaishnavu@nuvepro.com
#gituhb-Repo: https://github.com/vaishnavucv/Palo-Alto-VM-config
import subprocess

# Install necessary packages
required_packages = ["paramiko", "requests", "colorama", "urllib3"]
for package in required_packages:
    subprocess.check_call([subprocess.sys.executable, "-m", "pip", "install", package])

import paramiko
import socket
import requests
import webbrowser
import time
from colorama import init, Fore

init(autoreset=True)  # Initialize colorama to auto-reset the style

# Constants
VBOXMANAGE_PATH = '/usr/bin/VBoxManage'
VM_NAME = "PA-VM-9.0.4"
SSH_PORT = 22
SSH_USERNAME = "admin"
SSH_PASSWORD = "Password123$"
IP_ADDRESSES = ["192.168.56.100", "192.168.56.101", "192.168.56.103"]
VM_COMMAND = "show interface management"

def log_message(message, color=Fore.WHITE):
    """Print colored messages to the terminal."""
    print(color + message)

def is_vm_running():
    """Check if the specified VM is running."""
    try:
        output = subprocess.check_output([VBOXMANAGE_PATH, 'list', 'runningvms'], text=True)
        return VM_NAME in output
    except subprocess.CalledProcessError:
        return False

def is_port_open(ip, port):
    """Check if a port is open on the given IP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def ssh_and_check_ip(ip):
    """Attempt SSH connection, run commands, and check response."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=SSH_USERNAME, password=SSH_PASSWORD, port=SSH_PORT)
        log_message(f"Connected to {ip}", Fore.GREEN)
        shell = client.invoke_shell()
        shell.send(VM_COMMAND + "\n")
        time.sleep(5)
        shell.send("exit\n")
        time.sleep(1)
        output = shell.recv(50000).decode('utf-8')
        log_message(f"Output for {ip}: {output[:500]}", Fore.CYAN)
        if ip in output:
            log_message(f"VM is configured and IP of the VM: {ip}", Fore.YELLOW)
            return True
    except paramiko.SSHException as e:
        log_message(f"SSH connection failed to {ip}: {e}", Fore.RED)
    finally:
        client.close()
    return False

def check_web_accessibility(ip):
    """Check if the web dashboard is accessible."""
    try:
        response = requests.get(f"https://{ip}", verify=False, timeout=10)
        if response.status_code == 200:
            log_message("Web dashboard is configured and accessible.", Fore.GREEN)
            return True
    except requests.RequestException as e:
        log_message(f"Web dashboard is not accessible: {e}", Fore.RED)
    return False

def open_firefox(url):
    """Open a URL in Firefox."""
    log_message(f"Opening Firefox at {url}", Fore.BLUE)
    webbrowser.get('firefox').open(url)

def main():
    log_message("Checking if the VM is running...", Fore.MAGENTA)
    if not is_vm_running():
        log_message(f"VM {VM_NAME} is not running.", Fore.RED)
        return

    for ip in IP_ADDRESSES:
        log_message(f"Checking port {SSH_PORT} on {ip}...", Fore.MAGENTA)
        if is_port_open(ip, SSH_PORT):
            if ssh_and_check_ip(ip):
                if check_web_accessibility(ip):
                    open_firefox(f"https://{ip}")
                break
        else:
            log_message(f"{ip} port {SSH_PORT} is not open.", Fore.YELLOW)
    else:
        log_message("No IP addresses were successfully connected for SSH.", Fore.RED)

if __name__ == "__main__":
    main()
