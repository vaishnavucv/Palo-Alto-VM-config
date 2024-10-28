# Palo-Alto-VM-config

# VirtualBox VM Management Script

This script is designed to manage a specific VirtualBox VM, "PA-VM-9.0.4", running on an Ubuntu host. It checks if the VM is running, configures it using a series of SSH commands, and opens a Firefox window to a specified IP address for management purposes.

## Features

- Checks if "PA-VM-9.0.4" is running on VirtualBox.
- Configures the VM's network settings using SSH.
- Opens Firefox at "https://192.168.56.100" for VM management.

## Prerequisites

Before running this script, ensure you have the following installed:
- Python 3.x
- VirtualBox
- Firefox
- `paramiko` Python library (The script will attempt to install this if it's not present).

## Installation

1. Clone this repository or download the script to your local machine:
   ```bash
   git clone https://github.com/vaishnavucv/Palo-Alto-VM-config/ && sudo apt-get install python3-paramiko -y
   ```
2. Ensure you have Python installed.
3. Run the script as a user with permission to execute VBoxManage commands.
4. Usage
-  To use the script, simply run it from your terminal:
  ```bash
  cd Palo-Alto-VM-config
  chmod +x Palo-VM-config.py
  python3 Palo-VM-config.py
  ```
- Make sure to modify the script constants like SSH_IP, SSH_USERNAME, and SSH_PASSWORD to match your VM's configuration.

## Contributing

  . Contributions to this project are welcome! Please fork the repository and submit a pull request with your enhancements.
License
  - This project is licensed under the MIT License - see the LICENSE.md file for details.


